# 第五届“鹏城杯”初赛 Reverse-MDriver-赛题解析

> 原文: https://www.ctfiot.com/291134.html
> ID: 291134

驱动分析

voidClassifyFn(constFWPS_INCOMING_VALUES0 *inFixedValues, // a1constFWPS_INCOMING_METADATA_VALUES0 *inMetaValues,// a2void*layerData, // a3constvoid*classifyContext, // a4constFWPS_FILTER1 *filter, // a5 UINT64 flowContext, // a6 (IDA识别为 _DWORD* 有误) FWPS_CLASSIFY_OUT0 *classifyOut // a7);

1: kd> rdmsr C0000082msr[c0000082] = fffff801`0c2119001: kd> db fffff801`0c211900 l4fffff801`0c211900 0f 01 f8 65（key1！！）

defgenerate_v4_key():# 1. 准备种子字符串 "C:WINDOWS" (宽字符, 大写)# 来源于之前的分析：KUSER_SHARED_DATA.NtSystemRoot seed_str ="C:\WINDOWS" seed_bytes = seed_str.encode('utf-16le') seed_bytes = seed_bytes[:0x14]print(f"[*] 种子数据 (Hex):{seed_bytes.hex().upper()}") v4 =bytearray(256)forkinrange(len(seed_bytes)): v4[k] = seed_bytes[k]print("[*] 开始计算密钥流 v4...")foriinrange(256): not_i = (~i) &0xFF v4[i] ^= not_i# 5. 输出结果print("-"*30)print(f"[+] 最终密钥 v4 (256 bytes) 生成完成。")print("-"*30)print("前 40 字节预览 (Hex):")print(v4[:40].hex(' ').upper())print("n[C 语言数组格式]:") c_array =', '.join([f'0x{b:02X}'forbinv4])print(f"unsigned char v4[256] = {{{c_array}}};")returnv4if__name__ =="__main__": key_stream = generate_v4_key()

反调试分析

EXP

defsolve_payload():# 1. 密文 (v41) - 20 字节 cipher = [0xD4,0x90,0x60,0xED,0xC7,0xA4,0x30,0xF4,0xDF,0x93,0x1C,0xE5,0xD0,0x96,0x19,0xF3,0xDB,0x8E,0x21,0xA8 ]# 2. Key 1 (MSR Key) - 4 字节循环# 来源于 KiSystemCall64 前4字节 key1 = [0x0F,0x01,0xF8,0x65]# 3. Key 2 (Seed Key / v4) - 取前 20 字节# 来源于 C:WINDOWS 异或处理 key2 = [0xBC,0xFE,0xC7,0xFC,0xA7,0xFA,0xAE,0xF8,0xBE,0xF6,0xBB,0xF4,0xB7,0xF2,0xBE,0xF0,0xB8,0xEE,0xBE,0xEC ] payload = []foriinrange(len(cipher)): c = cipher[i] k2 = key2[i] k1 = key1[i %4] # 循环取 Key1 p = c ^ k2 ^ k1 payload.append(p)print("-"*60)# 输出最终结果 payload_str ="".join([chr(x)forxinpayload]) payload_hex =" ".join([f"{x:02X}"forxinpayload])print(f"[+] 最终 Key (Hex) :{payload_hex}")print(f"[+] 最终 Key (String):{payload_str}")if__name__ =="__main__": solve_payload()

importsocketimportstructimporttimeimportosdefchecksum(data):iflen(data) %2: data +=b'x00' res =sum(struct.unpack('!%sH'% (len(data) //2), data)) res = (res >>16) + (res &0xffff) res += res >>16return(~res) &0xffffdefsend_final_exploit(): target_ip ="127.0.0.1"print(f"[*] Target IP:{target_ip}") key =b'go_to_find_the_flag!' icmp_type =8 icmp_code =0 icmp_id = os.getpid() &0xFFFF icmp_seq =1 header_no_chk = struct.pack('!BBHHH', icmp_type, icmp_code,0, icmp_id, icmp_seq) chk = checksum(header_no_chk + key)# 填入校验和 header = struct.pack('!BBHHH', icmp_type, icmp_code, chk, icmp_id, icmp_seq) packet = header + keytry: s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) s.sendto(packet, (target_ip,0))print(f"[+] Packet Sent! Type={icmp_type}, Payload='{key.decode()}'")print("[*] 驱动触发")exceptExceptionase:print(f"[X] 发送失败:{e}")if__name__ =="__main__": send_final_exploit()input("n[!] 进程已暂停。n按回车键退出...")

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
```



```
1: kd> rdmsr C0000082msr[c0000082] = fffff801`0c2119001: kd> db fffff801`0c211900 l4fffff801`0c211900 0f 01 f8 65（key1！！）
```



```
defgenerate_v4_key():# 1. 准备种子字符串 "C:WINDOWS" (宽字符, 大写)# 来源于之前的分析：KUSER_SHARED_DATA.NtSystemRoot seed_str ="C:\WINDOWS" seed_bytes = seed_str.encode('utf-16le') seed_bytes = seed_bytes[:0x14]print(f"[*] 种子数据 (Hex):{seed_bytes.hex().upper()}") v4 =bytearray(256)forkinrange(len(seed_bytes)): v4[k] = seed_bytes[k]print("[*] 开始计算密钥流 v4...")foriinrange(256): not_i = (~i) &0xFF v4[i] ^= not_i# 5. 输出结果print("-"*30)print(f"[+] 最终密钥 v4 (256 bytes) 生成完成。")print("-"*30)print("前 40 字节预览 (Hex):")print(v4[:40].hex(' ').upper())print("n[C 语言数组格式]:") c_array =', '.join([f'0x{b:02X}'forbinv4])print(f"unsigned char v4[256] = {{{c_array}}};")returnv4if__name__ =="__main__": key_stream = generate_v4_key()
```



```
defsolve_payload():# 1. 密文 (v41) - 20 字节 cipher = [0xD4,0x90,0x60,0xED,0xC7,0xA4,0x30,0xF4,0xDF,0x93,0x1C,0xE5,0xD0,0x96,0x19,0xF3,0xDB,0x8E,0x21,0xA8 ]# 2. Key 1 (MSR Key) - 4 字节循环# 来源于 KiSystemCall64 前4字节 key1 = [0x0F,0x01,0xF8,0x65]# 3. Key 2 (Seed Key / v4) - 取前 20 字节# 来源于 C:WINDOWS 异或处理 key2 = [0xBC,0xFE,0xC7,0xFC,0xA7,0xFA,0xAE,0xF8,0xBE,0xF6,0xBB,0xF4,0xB7,0xF2,0xBE,0xF0,0xB8,0xEE,0xBE,0xEC ] payload = []foriinrange(len(cipher)): c = cipher[i] k2 = key2[i] k1 = key1[i %4] # 循环取 Key1 p = c ^ k2 ^ k1 payload.append(p)print("-"*60)# 输出最终结果 payload_str ="".join([chr(x)forxinpayload]) payload_hex =" ".join([f"{x:02X}"forxinpayload])print(f"[+] 最终 Key (Hex) :{payload_hex}")print(f"[+] 最终 Key (String):{payload_str}")if__name__ =="__main__": solve_payload()
```



```
importsocketimportstructimporttimeimportosdefchecksum(data):iflen(data) %2: data +=b'x00' res =sum(struct.unpack('!%sH'% (len(data) //2), data)) res = (res >>16) + (res &0xffff) res += res >>16return(~res) &0xffffdefsend_final_exploit(): target_ip ="127.0.0.1"print(f"[*] Target IP:{target_ip}") key =b'go_to_find_the_flag!' icmp_type =8 icmp_code =0 icmp_id = os.getpid() &0xFFFF icmp_seq =1 header_no_chk = struct.pack('!BBHHH', icmp_type, icmp_code,0, icmp_id, icmp_seq) chk = checksum(header_no_chk + key)# 填入校验和 header = struct.pack('!BBHHH', icmp_type, icmp_code, chk, icmp_id, icmp_seq) packet = header + keytry: s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) s.sendto(packet, (target_ip,0))print(f"[+] Packet Sent! Type={icmp_type}, Payload='{key.decode()}'")print("[*] 驱动触发")exceptExceptionase:print(f"[X] 发送失败:{e}")if__name__ =="__main__": send_final_exploit()input("n[!] 进程已暂停。n按回车键退出...")
```



```
flag{Y0r_Ar3_W1nKern3l_Mas7er!*}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767866945-wxsync-2026-01-b028272905f4fd07329d484b64696a86.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767866947-wxsync-2026-01-b028272905f4fd07329d484b64696a86.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767866948-wxsync-2026-01-1d4b7a1a1966126c5153683badcab87a.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767866950-wxsync-2026-01-69b34e253053e431bb42bd5e81108330.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767866952-wxsync-2026-01-6c232b78471c082e8a9c5e58eb949fa3.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767866954-wxsync-2026-01-8984a6fcf5b9b1088a319a5a4e7b6c9a.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767866955-wxsync-2026-01-e85c4e8236842f5d2b24a244c4c994f6.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767866957-wxsync-2026-01-66e59b824d6d178a2ca03f266dc4038c.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767866959-wxsync-2026-01-c20a406519a4cdaeeeb92f3d8bc35599.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1767866960-wxsync-2026-01-86fbbf3b1ce0a2ce26d2ac8af4931581.jpg)