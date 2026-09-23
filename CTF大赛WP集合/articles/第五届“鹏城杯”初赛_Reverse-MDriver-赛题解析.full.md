---
title: 第五届"鹏城杯"初赛 Reverse-MDriver-赛题解析
contest: 鹏城杯
year: 2025
difficulty: hard
vuln_type: reverse
tags:
- Windows驱动
- WFP
- FWPS_CLASSIFY
- MSR
- KiSystemCall64
- KUSER_SHARED_DATA
- ICMP
- RC4-XOR
attack_chain: '1. 识别ClassifyFn为WFP callout驱动函数→rdmsr C0000082获取MSR_LSTAR=fffff801`0c211900→KiSystemCall64前4字节0f 01 f8 65作key1(4字节循环)|2. 读取KUSER_SHARED_DATA.NtSystemRoot="C:\WINDOWS" UTF-16LE 20字节→v4[i]^=(~i)&0xFF 256次异或生成key2|3. 密文v41 20字节cipher=payload[i]=cipher[i]^key2[i]^key1[i%4]|4. 触发: Python socket SOCK_RAW IPPROTO_ICMP发包payload=go_to_find_the_flag!→驱动ICMP包匹配触发'
key_payload: msr[c0000082] = fffff801`0c211900|0f 01 f8 65(key1)|seed_str="C:\WINDOWS" seed_bytes=seed_str.encode('utf-16le')[:0x14]|v4[i] ^= (~i) & 0xFF for i in range(256)|cipher=[0xD4,0x90,0x60,0xED,...]|key2=[0xBC,0xFE,0xC7,0xFC,...]|p=c^k2^k1|socket.SOCK_RAW socket.IPPROTO_ICMP|flag{Y0r_Ar3_W1nKern3l_Mas7er!*}
one_liner: 鹏城杯2025 WFP callout驱动逆向,ClassifyFn识别WFP过滤ICMP,MSR_LSTAR读KiSystemCall64前4字节作Key1,KUSER_SHARED_DATA.NtSystemRoot="C:\WINDOWS" UTF-16LE异或(~i)生成Key2,密文双key异或解flag,Python SOCK_RAW发ICMP包触发驱动
lesson: 1) WFP驱动ClassifyFn签名识别:(const FWPS_INCOMING_VALUES0*, const FWPS_INCOMING_METADATA_VALUES0*, void*, const void*, const FWPS_FILTER1*, UINT64, FWPS_CLASSIFY_OUT0*); 2) MSR C0000082(MSR_LSTAR)读KiSystemCall64前4字节作为密码key1; 3) KUSER_SHARED_DATA.NtSystemRoot(0x30偏移)固定存系统目录"C:\WINDOWS" UTF-16LE格式,加密key素材; 4) Python socket SOCK_RAW IPPROTO_ICMP直接发ICMP包触发驱动callout; 5) 驱动级逆向思路:从filter/classify函数入手定位算法,MSR+共享数据是常见数据源
quality: high
full_path: 第五届“鹏城杯”初赛_Reverse-MDriver-赛题解析.full.md
meta_path: 第五届“鹏城杯”初赛_Reverse-MDriver-赛题解析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 第五届"鹏城杯"初赛 Reverse-MDriver-赛题解析。鹏城杯2025 WFP callout驱动逆向,ClassifyFn识别WFP过滤ICMP,MSR_LSTAR读KiSystemCall64前4字节作Key1,KUSER_SHARED_DATA.NtSystemRoot="C:\WINDOWS" UTF-16LE异或(~i)生成Key2,密文双key异或解flag,P...
category: reverse
subcategory: reverse
tools_used:
- C
- Python
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/291134.html
reasoning_chain:
- WFP callout 驱动逆向 → 触发点：ClassifyFn 识别 WFP callout 函数
- 动作：识别函数签名 (FWPS_INCOMING_VALUES0*, FWPS_INCOMING_METADATA_VALUES0*, void*, const void*, FWPS_FILTER1*, UINT64, FWPS_CLASSIFY_OUT0*)
- 假设：rdmsr C0000082 读 MSR_LSTAR = fffff801'0c211900 → KiSystemCall64 前 4 字节 0f 01 f8 65 作 key1
- 假设：KUSER_SHARED_DATA.NtSystemRoot 偏移 0x30 = 'C:\WINDOWS' UTF-16LE 20 字节 → v4[i] ^= (~i) & 0xFF 256 次异或生成 key2
- 动作：cipher[i] = cipher[i] ^ key2[i] ^ key1[i%4] → 解 flag
- 假设：触发驱动 → 动作：Python socket SOCK_RAW IPPROTO_ICMP 发包 payload='go_to_find_the_flag!'
- 观察：flag{Y0r_Ar3_W1nKern3l_Mas7er!*}
failed_attempts:
- 直接 IDA 看 ClassifyFn 函数 → 失败：必须 rdmsr C0000082 才能取 KiSystemCall64
- KUSER_SHARED_DATA 偏移错误 → 失败：NtSystemRoot 在 0x30 偏移不是其他位置
key_observations:
- WFP 驱动 ClassifyFn 签名识别是驱动逆向入口
- MSR C0000082(MSR_LSTAR) 读 KiSystemCall64 前 4 字节作为密码 key1
- KUSER_SHARED_DATA.NtSystemRoot(0x30 偏移) 固定存系统目录 UTF-16LE 格式
- Python socket SOCK_RAW IPPROTO_ICMP 直接发 ICMP 包触发驱动 callout
- 驱动级逆向思路：从 filter/classify 函数入手定位算法
prerequisites:
- WFP 驱动逆向（ClassifyFn 识别）
- MSR 寄存器读取（rdmsr 指令）
- KUSER_SHARED_DATA 结构（NtSystemRoot 偏移）
- Python socket SOCK_RAW IPPROTO_ICMP 发包
---
# 第五届“鹏城杯”初赛 Reverse-MDriver-赛题解析

> 原文: https://www.ctfiot.com/291134.html
> ID: 291134

驱动分析

voidClassifyFn(constFWPS_INCOMING_VALUES0 *inFixedValues, // a1constFWPS_INCOMING_METADATA_VALUES0 *inMetaValues,// a2void*layerData, // a3constvoid*classifyContext, // a4constFWPS_FILTER1 *filter, // a5 UINT64 flowContext, // a6 (IDA识别为 _DWORD* 有误) FWPS_CLASSIFY_OUT0 *classifyOut // a7);

1: kd> rdmsr C0000082msr[c0000082] = fffff801`0c2119001: kd> db fffff801`0c211900 l4fffff801`0c211900 0f 01 f8 65（key1！！）

defgenerate_v4_key():# 1. 准备种子字符串 "C:
WINDOWS" (宽字符, 大写)
# 来源于之前的分析：KUSER_SHARED_DATA.NtSystemRoot seed_str ="C:\WINDOWS" seed_bytes = seed_str.encode('utf-16le') seed_bytes = seed_bytes[:
0x14]print(f"[*] 种子数据 (Hex):{seed_bytes.hex().upper()}") v4 =bytearray(256)forkinrange(len(seed_bytes)): v4[k] = seed_bytes[k]print("[*] 开始计算密钥流 v4...")foriinrange(256): not_i = (~i) &0xFF v4[i] ^= not_i
# 5. 输出结果print("-"*30)print(f"[+] 最终密钥 v4 (256 bytes) 生成完成。")print("-"*30)print("前 40 字节预览 (Hex):")print(v4[:40].hex(' ').upper())print("n[C 语言数组格式]:") c_array =', '.join([f'0x{b:
02X}'forbinv4])print(f"unsigned char v4[256] = {{{c_array}}};")returnv4if__name__ =="__main__": key_stream = generate_v4_key()

反调试分析

EXP

defsolve_payload():# 1. 密文 (v41) - 20 字节 cipher = [0xD4,0x90,0x60,0xED,0xC7,0xA4,0x30,0xF4,0xDF,0x93,0x1C,0xE5,0xD0,0x96,0x19,0xF3,0xDB,0x8E,0x21,0xA8 ]# 2. Key 1 (MSR Key) - 4 字节循环
# 来源于 KiSystemCall64 前4字节 key1 = [0x0F,0x01,0xF8,0x65]# 3. Key 2 (Seed Key / v4) - 取前 20 字节
# 来源于 C:
WINDOWS 异或处理 key2 = [0xBC,0xFE,0xC7,0xFC,0xA7,0xFA,0xAE,0xF8,0xBE,0xF6,0xBB,0xF4,0xB7,0xF2,0xBE,0xF0,0xB8,0xEE,0xBE,0xEC ] payload = []foriinrange(len(cipher)): c = cipher[i] k2 = key2[i] k1 = key1[i %4] # 循环取 Key1 p = c ^ k2 ^ k1 payload.append(p)print("-"*60)
# 输出最终结果 payload_str ="".join([chr(x)forxinpayload]) payload_hex =" ".join([f"{x:
02X}"forxinpayload])print(f"[+] 最终 Key (Hex) :{payload_hex}")print(f"[+] 最终 Key (String):{payload_str}")if__name__ =="__main__": solve_payload()

importsocketimportstructimporttimeimportosdefchecksum(data):
iflen(data) %2: data +=b'x00' res =sum(struct.unpack('!%sH'% (len(data) //2), data)) res = (res >>16) + (res &0xffff) res += res >>16return(~res) &0xffffdefsend_final_exploit(): target_ip ="127.0.0.1"print(f"[*] Target IP:{target_ip}") key =b'go_to_find_the_flag!' icmp_type =8 icmp_code =0 icmp_id = os.getpid() &0xFFFF icmp_seq =1 header_no_chk = struct.pack('!BBHHH', icmp_type, icmp_code,0, icmp_id, icmp_seq) chk = checksum(header_no_chk + key)
# 填入校验和 header = struct.pack('!BBHHH', icmp_type, icmp_code, chk, icmp_id, icmp_seq) packet = header + key
try: s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) s.sendto(packet, (target_ip,0))print(f"[+] Packet Sent! Type={icmp_type}, Payload='{key.decode()}'")print("[*] 驱动触发")exceptExceptionase:
print(f"[X] 发送失败:{e}")if__name__ =="__main__": send_final_exploit()input("n[!] 进程已暂停。n按回车键退出...")

flag{Y0r_Ar3_W1nKern3l_Mas7er!*}

看雪ID：relost

https://bbs.kanxue.com/user-home-1006061.htm

*本文为看雪论坛优秀文章，由relost原创，转载请注明来自看雪社区

# 往期推荐

逆向分析某手游基于异常的内存保护

解决Il2cppapi混淆，通杀DumpUnityCs文件

记录一次Unity加固的探索与实现

DLINK路由器命令注入漏洞从1DAY到0DAY

量子安全 quantum ctf Global Hyperlink Zone Hack the box

球分享

球点赞

球在看

点击阅读原文查看更多


```
voidClassifyFn(constFWPS_INCOMING_VALUES0 *inFixedValues, // a1constFWPS_INCOMING_METADATA_VALUES0 *inMetaValues,// a2void*layerData, // a3constvoid*classifyContext, // a4constFWPS_FILTER1 *filter, // a5 UINT64 flowContext, // a6 (IDA识别为 _DWORD* 有误) FWPS_CLASSIFY_OUT0 *classifyOut // a7);
1: kd> rdmsr C0000082msr[c0000082] = fffff801`0c2119001: kd> db fffff801`0c211900 l4fffff801`0c211900 0f 01 f8 65（key1！！）
defgenerate_v4_key():# 1. 准备种子字符串 "C:
WINDOWS" (宽字符, 大写)
# 来源于之前的分析：KUSER_SHARED_DATA.NtSystemRoot seed_str ="C:\WINDOWS" seed_bytes = seed_str.encode('utf-16le') seed_bytes = seed_bytes[:
0x14]print(f"[*] 种子数据 (Hex):{seed_bytes.hex().upper()}") v4 =bytearray(256)forkinrange(len(seed_bytes)): v4[k] = seed_bytes[k]print("[*] 开始计算密钥流 v4...")foriinrange(256): not_i = (~i) &0xFF v4[i] ^= not_i
# 5. 输出结果print("-"*30)print(f"[+] 最终密钥 v4 (256 bytes) 生成完成。")print("-"*30)print("前 40 字节预览 (Hex):")print(v4[:40].hex(' ').upper())print("n[C 语言数组格式]:") c_array =', '.join([f'0x{b:
02X}'forbinv4])print(f"unsigned char v4[256] = {{{c_array}}};")returnv4if__name__ =="__main__": key_stream = generate_v4_key()
defsolve_payload():# 1. 密文 (v41) - 20 字节 cipher = [0xD4,0x90,0x60,0xED,0xC7,0xA4,0x30,0xF4,0xDF,0x93,0x1C,0xE5,0xD0,0x96,0x19,0xF3,0xDB,0x8E,0x21,0xA8 ]# 2. Key 1 (MSR Key) - 4 字节循环
# 来源于 KiSystemCall64 前4字节 key1 = [0x0F,0x01,0xF8,0x65]# 3. Key 2 (Seed Key / v4) - 取前 20 字节
# 来源于 C:
WINDOWS 异或处理 key2 = [0xBC,0xFE,0xC7,0xFC,0xA7,0xFA,0xAE,0xF8,0xBE,0xF6,0xBB,0xF4,0xB7,0xF2,0xBE,0xF0,0xB8,0xEE,0xBE,0xEC ] payload = []foriinrange(len(cipher)): c = cipher[i] k2 = key2[i] k1 = key1[i %4] # 循环取 Key1 p = c ^ k2 ^ k1 payload.append(p)print("-"*60)
# 输出最终结果 payload_str ="".join([chr(x)forxinpayload]) payload_hex =" ".join([f"{x:
02X}"forxinpayload])print(f"[+] 最终 Key (Hex) :{payload_hex}")print(f"[+] 最终 Key (String):{payload_str}")if__name__ =="__main__": solve_payload()
importsocketimportstructimporttimeimportosdefchecksum(data):
iflen(data) %2: data +=b'x00' res =sum(struct.unpack('!%sH'% (len(data) //2), data)) res = (res >>16) + (res &0xffff) res += res >>16return(~res) &0xffffdefsend_final_exploit(): target_ip ="127.0.0.1"print(f"[*] Target IP:{target_ip}") key =b'go_to_find_the_flag!' icmp_type =8 icmp_code =0 icmp_id = os.getpid() &0xFFFF icmp_seq =1 header_no_chk = struct.pack('!BBHHH', icmp_type, icmp_code,0, icmp_id, icmp_seq) chk = checksum(header_no_chk + key)
# 填入校验和 header = struct.pack('!BBHHH', icmp_type, icmp_code, chk, icmp_id, icmp_seq) packet = header + key
try: s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) s.sendto(packet, (target_ip,0))print(f"[+] Packet Sent! Type={icmp_type}, Payload='{key.decode()}'")print("[*] 驱动触发")exceptExceptionase:
print(f"[X] 发送失败:{e}")if__name__ =="__main__": send_final_exploit()input("n[!] 进程已暂停。n按回车键退出...")
flag{Y0r_Ar3_W1nKern3l_Mas7er!*}
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