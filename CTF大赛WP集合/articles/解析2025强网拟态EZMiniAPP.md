# 解析2025强网拟态EZMiniAPP

> 原文: https://www.ctfiot.com/278076.html
> ID: 278076

微信小程序逆向分析与加密算法破解

一、题目背景与初步分析

1.1 题目描述

本题是一道Mobile类别的CTF挑战题，题目提供了一个文件：__APP__.wxapkg。

1.2 什么是wxapkg文件

.wxapkg是微信小程序的打包文件格式。微信小程序是运行在微信客户端内的轻量级应用程序，其代码包就以这种特殊格式分发。

wxapkg文件的特点：

二进制格式，无法直接用文本编辑器查看

包含小程序的所有资源：JavaScript代码、页面模板、样式表、配置文件等

有特定的文件结构：包含文件头、索引区和数据区

解包wxapkg文件，提取其中的代码

分析JavaScript代码，找到加密逻辑

理解加密算法的工作原理

编写解密脚本，获取flag

多字节整数使用**大端序（Big-Endian）**存储

文件偏移量是从wxapkg文件开头计算的绝对位置

文件名是UTF-8编码的字符串

解析文件头，获取文件列表信息

根据偏移量和大小，提取每个文件的数据

还原成原始的目录结构

struct.unpack('B', data)：解包1个无符号字节

struct.unpack('>I', data)：解包4字节无符号整数（大端序）

>表示大端序

I表示无符号整数（unsigned int）

decode('utf-8')：将字节序列解码为UTF-8字符串

密钥："newKey2025!"

预期密文：[1, 33, 194, 133, 195, 102, 232, 104, 200, 14, 8, 163, 131, 71, 68, 97, 2, 76, 72, 171, 74, 106, 225, 1, 65]

加密函数：enigmaticTransformation

A ^ B = C则C ^ B = A（自反性）

A ^ 0 = A

A ^ A = 0

加密和解密使用相同的运算

简单高效

数学上具有对称性

循环左移的逆运算是循环右移

异或的逆运算仍是异或（因为(A ^ B) ^ B = A）

格式字符

C类型

Python类型

字节数

B

unsigned char

integer

1

H

unsigned short

integer

2

I

unsigned int

integer

4

Q

unsigned long long

integer

8

标识

字节序

说明

<

小端序

Little-Endian

>

大端序

Big-Endian

=

本机序

Native

交换律：A ^ B = B ^ A

结合律：(A ^ B) ^ C = A ^ (B ^ C)

自反性：A ^ B ^ B = A

恒等律：A ^ 0 = A

归零律：A ^ A = 0

分析每个分支的实际计算结果

简化位运算表达式

找出运算的数学本质

识别加密算法类型：对称/非对称、流密码/分组密码

提取关键参数：密钥、初始向量、轮数等

理解运算流程：每一步的数学含义

推导逆运算：找到每个步骤的逆操作

实现解密：编写代码实现逆运算

验证结果：重新加密检验

移动应用安全

Android APK逆向

iOS IPA分析

微信小程序/支付宝小程序

密码学

对称加密算法（AES、DES、RC4）

非对称加密算法（RSA、ECC）

哈希函数（MD5、SHA系列）

逆向工程

静态分析工具（IDA Pro、Ghidra）

动态调试（GDB、OllyDbg）

反编译技术

代码混淆

控制流平坦化

虚拟机保护

符号混淆

Python 3.x：脚本编写

wxappUnpacker：专业的微信小程序解包工具

VS Code：代码编辑器

010 Editor：十六进制编辑器

Frida：动态插桩框架

jadx：APK反编译

Hopper Disassembler：反汇编工具

文件格式分析：理解wxapkg的二进制结构

代码阅读：从混淆的JavaScript中提取关键逻辑

算法理解：掌握异或、循环移位等基本运算

逆向思维：从加密推导出解密过程

编程实现：用Python实现解密工具

分析恶意软件的通信加密

逆向闭源应用的协议

审计移动应用的安全性

破解软件的授权机制


```
┌─────────────────────────────────────┐│ 文件头部 (Header) │├─────────────────────────────────────┤│ - First Mark (1字节): 标识字节 ││ - Info1 (4字节): 信息段 ││ - Info2 (4字节): 信息段 ││ - Data Offset (4字节): 数据区偏移 ││ - Reserved (1字节): 保留字节 │├─────────────────────────────────────┤│ 索引区 (Index Section) │├─────────────────────────────────────┤│ - File Count (4字节): 文件数量 ││ - File List: 文件列表 ││ * Name Length (4字节) ││ * Name (变长): 文件名 ││ * Offset (4字节): 文件偏移 ││ * Size (4字节): 文件大小 │├─────────────────────────────────────┤│ 数据区 (Data Section) │├─────────────────────────────────────┤│ 各个文件的实际数据内容 │└─────────────────────────────────────┘
```



```
#!/usr/bin/env python3importstructimportosdefunpack_wxapkg(wxapkg_file, output_dir): """解包微信小程序 wxapkg 文件""" withopen(wxapkg_file,'rb')asf: # 读取头部信息 first_mark = struct.unpack('B', f.read(1))[0] f.read(4) # 跳过Info1 f.read(4) # 跳过Info2 # 读取数据区偏移量 (大端序，用'>I'表示) data_section_offset = struct.unpack('>I', f.read(4))[0] f.read(1) # 跳过保留字节 # 读取文件数量 file_count = struct.unpack('>I', f.read(4))[0] # 读取文件列表 file_list = [] foriinrange(file_count): # 文件名长度 name_len = struct.unpack('>I', f.read(4))[0] # 文件名 (UTF-8编码) name = f.read(name_len).decode('utf-8') # 文件偏移和大小 offset = struct.unpack('>I', f.read(4))[0] size = struct.unpack('>I', f.read(4))[0] file_list.append({ 'name': name, 'offset': offset, 'size': size }) # 创建输出目录 ifnotos.path.exists(output_dir): os.makedirs(output_dir) # 解包每个文件 forfile_infoinfile_list: name = file_info['name'].lstrip('/') file_path = os.path.join(output_dir, name) file_dir = os.path.dirname(file_path) # 创建文件所在目录 iffile_dirandnotos.path.exists(file_dir): os.makedirs(file_dir) # 读取并写入文件数据 f.seek(file_info['offset']) file_data = f.read(file_info['size']) withopen(file_path,'wb')asout_f: out_f.write(file_data) print(f"Extracted:{file_info['name']}")
```



```
python3 unpacker.py
```



```
Unpacking __APP__.wxapkg...First mark: 190Data section offset: 170832File count: 24File 1: /__debug__/__jscore-debug__.png, offset: 907, size: 178...File 11: /chunk_0.appservice.js, offset: 65008, size: 15834...Extracted: /chunk_0.appservice.js...Done!
```



```
unpacked/├── __debug__/ # 调试文件├── app-config.json # 小程序配置├── app-service.js # 服务层主文件├── appservice.app.js # 应用逻辑├── chunk_0.appservice.js # ★ 关键：包含页面逻辑├── chunk_1.appservice.js # 代码分块├── common.app.js # 公共代码├── pages/ # 页面目录│ ├── index/ # 首页│ │ ├── index.html│ │ └── index.wxss│ └── logs/ # 日志页│ ├── logs.html│ └── logs.wxss└── page-frame.html # 页面框架
```



```
{"entryPagePath":"pages/index/index.html","pages": ["pages/index/index","pages/logs/logs"], ...}
```



```
Page({ data: { inputValue:"", animationData: {} }, // 输入框变化处理 onInputChange:function(a){ this.setData({inputValue: a.detail.value}); }, // ★ 关键：加密函数 enigmaticTransformation:function(a, t){ // a: 明文 // t: 密钥 // ... 加密逻辑 ... }, // 自定义加密入口 customEncrypt:function(a, t){ returnthis.enigmaticTransformation(a, t); }, // ★ 验证逻辑 onCheck:function(){ vara =this.data.inputValue; if(""!== a.trim()) { vart =this.customEncrypt(a,"newKey2025!"); console.log(t); JSON.stringify(t) ===JSON.stringify([1,33,194,133,195,102,232,104,200,14,8,163,131,71,68,97,2,76,72,171,74,106,225,1,65]) ? wx.showToast({title:"Right",icon:"success",duration:2e3}) : wx.showToast({title:"Wrong",icon:"error",duration:2e3}); } }});
```



```
enigmaticTransformation:function(a, t){ // 步骤1: 将密钥转换为ASCII码数组 i =Array.from(t).map(function(a){ returna.charCodeAt(0); }); s = i.length; // 步骤2: 计算循环移位参数c c =function(a){ for(vart =0, e =0; e < a.length; e++) { switch(e %4) { case0: t +=1* a[e];break; case1: t += a[e] +0;break; case2: t +=0| a[e];break; // 按位或0 case3: t +=0^ a[e];break; // 按位异或0 } } returnt; }(i) %8; // 步骤3: 逐字符加密 r = []; for(o =0; o < a.length; o++) { varu; // 3.1: 异或运算 switch(o %3) { case0: u = a.charCodeAt(o) ^ i[o % s]; break; case1: u = i[o % s] ^ a.charCodeAt(o); break; case2: e = a.charCodeAt(o); n = i[o % s]; u = e ^ n; break; } // 3.2: 循环左移 varh; switch(c) { case0: h = u;break; case1: h =255& (u <<1| u >>7&1);break; case2: h =255& (u <<2| u >>6&3);break; case3: h =255& (u <<3| u >>5&7);break; case4: h =255& (u <<4| u >>4&15);break; case5: h =255& (u <<5| u >>3&31);break; case6: h =255& (u <<6| u >>2&63);break; case7: h =255& (u <<7| u >>1&127);break; default: h =255& (u << c | u >> (8- c));break; } // 3.3: 添加到结果数组 r.push(h); } returnr;}
```



```
输入: 明文字符串, 密钥字符串 ↓步骤1: 密钥处理 - 将密钥转为ASCII码数组 - key = "newKey2025!" → [110, 101, 119, 75, 101, 121, 50, 48, 50, 53, 33] ↓步骤2: 计算移位参数 - 对密钥数组各元素求和 - sum = 110+101+119+75+101+121+50+48+50+53+33 = 861 - c = 861 % 8 = 5 ↓步骤3: 逐字符加密 对于每个明文字符: 3.1 异或运算 - plain_char ^ key[i % key_length] → u 3.2 循环左移 - rotate_left(u, c) → h 3.3 添加到结果 - result.append(h) ↓输出: 密文字节数组
```



```
case0: u = a.charCodeAt(o) ^ i[o % s];case1: u = i[o % s] ^ a.charCodeAt(o);case2: u = (a.charCodeAt(o)) ^ (i[o % s]);
```



```
原始: a b c d e f g h ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓左移3位: d e f g h a b c
```



```
h =255& (u <<5| u >>3&31)
```



```
假设 u = 0b10110011 (179)步骤1: u << 5 (左移5位) 10110011 → 01100000 (96) (左侧5位溢出)步骤2: u >> 3 (右移3位，8-5=3) 10110011 → 00010110 (22)步骤3: (u >> 3) & 31 (取低5位) 00010110 & 00011111 = 00010110 (22)步骤4: 左移结果 | 右移结果 01100000 | 00010110 = 01110110 (118)步骤5: & 255 (确保在0-255范围) 01110110 & 11111111 = 01110110 (118)结果: 10110011 循环左移5位 → 01110110
```



```
原始字节: 1 0 1 1 0 0 1 1 ╰─────────╯╰──╯ ↓ ↓左移5位后: 0 1 1 0 0 0 0 0 (左移部分) ↓右移3位后: 0 0 0 1 0 1 1 0 (溢出部分) ↓ 按位或最终结果: 0 1 1 1 0 1 1 0
```



```
明文字符: 'f' ↓1. 获取ASCII码 'f' → 102 → 0b011001102. 异或运算 (位置0，使用key[0]='n'=110) 102 ^ 110 = 0b01100110 ^ 0b01101110 = 0b00001000 = 83. 循环左移5位 u = 8 = 0b00001000 左移5位: 8 << 5 = 0b00000000 = 0 右移3位: 8 >> 3 = 0b00000001 = 1 取低5位: 1 & 31 = 1 按位或: 0 | 1 = 1 h = 14. 输出密文 cipher[0] = 1 ✓
```



```
defrot_right(x, n): """ 循环右移函数 参数: x: 待移位的字节值 n: 右移位数 返回: 循环右移n位后的结果 """ x &=0xFF# 确保在0-255范围内 return((x >> n) | (x << (8- n))) &0xFF
```



```
循环右移 = 右移n位 | 左移(8-n)位例如右移5位:原始: a b c d e f g h ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓右移5位: 0 0 0 0 0 a b c (右侧5位溢出)左移3位: f g h 0 0 0 0 0 (将溢出位移回) ↓ 按位或结果: f g h 0 0 a b c
```



```
defdecrypt(cipher, key): """ 解密函数 参数: cipher: 密文字节数组 key: 密钥字符串 返回: 解密后的明文字符串 """ # 步骤1: 密钥转ASCII码数组 key_array = [ord(c)forcinkey] key_length = len(key_array) # 步骤2: 计算移位参数 (与加密时相同) c = sum(key_array) %8 # 步骤3: 逐字节解密 plaintext = [] forposition, cipher_byteinenumerate(cipher): cipher_byte &=0xFF # 3a: 还原循环左移 → 执行循环右移 after_rotate = rot_right(cipher_byte, c) # 3b: 还原异或 (异或是自反运算) plain_code = after_rotate ^ key_array[position % key_length] # 3c: 转换为字符 plaintext.append(chr(plain_code)) return''.join(plaintext)
```



```
# 从小程序代码中提取的数据cipher = [1,33,194,133,195,102,232,104,200,14,8,163,131,71,68,97,2,76,72,171,74,106,225,1,65]key ="newKey2025!"# 解密flag = decrypt(cipher, key)print(f"Flag:{flag}")
```



```
======================================================================CTF题目: EZMiniAPP - 微信小程序逆向解密======================================================================[输入] 密文数组: [1, 33, 194, 133, 195, 102, 232, 104, 200, 14, 8, 163, 131, 71, 68, 97, 2, 76, 72, 171, 74, 106, 225, 1, 65] 长度: 25 字节[输入] 密钥: newKey2025! 长度: 11 字符======================================================================开始解密...======================================================================[调试] 密钥ASCII码数组: [110, 101, 119, 75, 101, 121, 50, 48, 50, 53, 33][调试] 密钥数组和: 861[调试] 移位参数c: 5[调试] 位置0: 密文字节: 1 (0b00000001) 右移5位后: 8 (0b00001000) 密钥字节: 110 异或结果: 102 (ASCII: 'f')[调试] 位置1: 密文字节: 33 (0b00100001) 右移5位后: 9 (0b00001001) 密钥字节: 101 异或结果: 108 (ASCII: 'l')[调试] 位置2: 密文字节: 194 (0b11000010) 右移5位后: 22 (0b00010110) 密钥字节: 119 异或结果: 97 (ASCII: 'a')======================================================================解密完成!======================================================================[结果] Flag: flag{JustEasyMiniProgram}======================================================================
```



```
defencrypt(plaintext, key): """完整复现JavaScript的加密算法""" key_array = [ord(c)forcinkey] key_length = len(key_array) c = sum(key_array) %8 result = [] forpositioninrange(len(plaintext)): # 异或 plain_code = ord(plaintext[position]) u = plain_code ^ key_array[position % key_length] # 循环左移 ifc ==5: h =255& (u <<5| u >>3&31) # ... 其他case ... result.append(h) returnresult# 验证encrypted = encrypt("flag{JustEasyMiniProgram}","newKey2025!")original = [1,33,194,133,195,102,232,104,200,14,8,163,131,71,68,97,2,76,72,171,74,106,225,1,65]ifencrypted == original: print("✓ 验证成功！解密结果正确！")
```



```
======================================================================加密验证 - 验证解密结果的正确性======================================================================[输入] 明文: flag{JustEasyMiniProgram}[输入] 密钥: newKey2025![输出] 加密结果: [1, 33, 194, 133, 195, 102, 232, 104, 200, 14, 8, 163, 131, 71, 68, 97, 2, 76, 72, 171, 74, 106, 225, 1, 65][对比] 原始密文: [1, 33, 194, 133, 195, 102, 232, 104, 200, 14, 8, 163, 131, 71, 68, 97, 2, 76, 72, 171, 74, 106, 225, 1, 65]======================================================================✓ 验证成功！解密结果正确！======================================================================Flag: flag{JustEasyMiniProgram}
```



```
# 大端序读取4字节无符号整数offset = struct.unpack('>I', f.read(4))[0]# 小端序读取2字节无符号短整数value = struct.unpack('<H', f.read(2))[0]
```



```
0 ^ 0 = 00 ^ 1 = 11 ^ 0 = 11 ^ 1 = 0
```



```
# 加密cipher = plaintext ^ key# 解密（使用相同的key）plaintext = cipher ^ key# 证明：# plaintext ^ key ^ key = plaintext
```



```
x << n # 左移n位，右侧补05 << 2 # 0b00000101 → 0b00010100 (5 → 20)
```



```
x >> n # 右移n位，左侧补020 >> 2 # 0b00010100 → 0b00000101 (20 → 5)
```



```
# 循环左移n位defrotate_left(x, n): return((x << n) | (x >> (8- n))) &0xFF# 循环右移n位defrotate_right(x, n): return((x >> n) | (x << (8- n))) &0xFF
```



```
x &0xFF # 保留低8位 (0-255)x &0x0F # 保留低4位 (0-15)x &0x01 # 保留最低位 (0或1)# 示例value =0b11010110low_4_bits = value &0x0F# 0b00000110 = 6
```



```
switch(e %4) { case0: t +=1* a[e];break; // 等价于 t += a[e] case1: t += a[e] +0;break; // 等价于 t += a[e] case2: t +=0| a[e];break; // 等价于 t += a[e] case3: t +=0^ a[e];break; // 等价于 t += a[e]}
```



```
switch(o %3) { case0: u = a ^ b;break; case1: u = b ^ a;break; // 与case 0相同 case2: u = a ^ b;break; // 与case 0相同}
```



```
┌─────────────────┐│ 静态分析 │ 阅读代码，理解逻辑├─────────────────┤│ 动态分析 │ 运行代码，观察行为├─────────────────┤│ 数学分析 │ 找出运算的逆运算├─────────────────┤│ 验证测试 │ 确认解密正确性└─────────────────┘
```



```
第一步：文件分析 ├─ 识别wxapkg格式 └─ 了解文件结构第二步：解包提取 ├─ 编写解包工具 (Python + struct) ├─ 解析文件头和索引 └─ 提取所有文件第三步：代码定位 ├─ 查看小程序配置 ├─ 找到入口页面 └─ 定位加密函数第四步：算法分析 ├─ 提取enigmaticTransformation函数 ├─ 理解加密流程 │ ├─ 密钥处理 │ ├─ 参数计算 │ └─ 逐字符加密 └─ 识别代码混淆第五步：逆向解密 ├─ 推导逆运算 │ ├─ 循环左移 → 循环右移 │ └─ 异或 → 异或 ├─ 实现解密函数 └─ 获取flag第六步：验证结果 ├─ 实现加密函数 ├─ 重新加密flag └─ 对比原始密文
```
