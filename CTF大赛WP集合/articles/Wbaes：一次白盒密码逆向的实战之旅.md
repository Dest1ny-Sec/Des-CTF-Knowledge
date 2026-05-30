# Wbaes：一次白盒密码逆向的实战之旅

> 原文: https://www.ctfiot.com/282908.html
> ID: 282908

Wbaes：一次白盒密码逆向的实战之旅

前言

白盒密码学(White-Box Cryptography)是现代密码学中的前沿领域，它要求即使在攻击者完全控制执行环境的情况下，密钥也不能被轻易提取。今天，我将带大家深入分析WHCTF 2017的一道高难度逆向题目——Wbaes，这道题完美地结合了白盒AES实现、MOVfuscation代码混淆技术，以及差分故障分析(DFA)攻击技术。

本文将以实战的方式，一步一步展示如何分析和破解这个看似不可能的挑战。

第一步：文件基本分析

拿到题目文件后，我首先要了解这是什么类型的程序。

查看文件信息

$ file WbaesWbaes: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, stripped$ ls -lh Wbaes-rwxr-xr-x 1 user user 9.3M Wbaes

立即引起注意的异常点：

文件大小达到9.3MB– 这对于一个普通的可执行程序来说极其异常

stripped– 没有符号信息，增加了逆向难度

32位ELF– 需要32位环境或兼容层

大量的查找表(Look-up Tables)

严重的代码混淆和膨胀

程序需要一个命令行参数作为输入

无论输入什么都没有输出

程序总是静默失败（退出码2）

memcmp– 用于比较结果，很可能比较加密结果和预期值

strlen– 检查输入长度

sigaction– 注册信号处理器，通常用于反调试

printf– 输出flag

9.3MB的文件大小– 白盒AES需要大量查找表来隐藏密钥

输入长度要求–strlen检查暗示固定长度输入，AES块大小是16字节

memcmp比较– 加密后的结果与预期值比较

算术运算（加减乘除）

逻辑运算（AND、OR、XOR）

控制流转移

静态分析几乎不可能 – 无法直观理解程序逻辑

动态调试困难 – 需要步进成千上万条指令

程序体积暴涨 – 简单操作被展开成数十条指令

输入必须是16字节（AES块大小）

程序内部硬编码了”正确的密文”

我们需要找到：什么明文加密后等于这个密文？

获取正常输出– 运行正常加密，得到正确密文

注入故障– 在加密过程中引入故障（修改字节、指令等）

收集故障输出– 记录故障导致的错误输出

差分分析– 分析正常输出和故障输出的差异，推导密钥

Deadpool– 自动化故障注入框架

PhoenixAES– AES密钥恢复工具

GDB调试– 失败：程序的sigaction检测到调试器后立即退出

静态分析查找memcmp– 失败：MOVfuscation隐藏了所有call指令

LD_PRELOAD Hook– 失败：缺少32位开发库

strace追踪– 失败：被反调试阻止

静态修改vs运行时内存– 修改磁盘文件不影响程序运行时加载的内存

PIE和ASLR– 现代保护机制使地址随机化

编译器优化– 代码被优化为故障抵抗的形式

验证密钥的正确性

在程序中找到加密的flag

用密钥解密得到flag

原字符

替换后

类型

w

W

大写

t

7

Leetspeak

f

F

大写

l

L

大写

a

@

符号替换

i

1

Leetspeak

程序异常大（MB级别）

包含大量数据段

逻辑简单但实现复杂

DRM系统

移动支付

软件授权

代码几乎全是MOV指令

体积膨胀数百倍

静态分析极其困难

动态追踪执行流程

关注输入输出关系

使用符号执行

学术研究使用专业硬件（激光、电压毛刺）

软件静态注入受现代保护机制限制

实际成功需要高级动态插桩工具

确认或获取加密密钥

在程序中搜索可能的加密数据

批量解密并筛选可读明文

验证候选结果

IDA Pro / Ghidra– 高级反汇编和反编译

Deadpool– DFA故障注入框架

PhoenixAES– AES密钥恢复

Intel PIN / Frida– 动态二进制插桩

理论与实践的差距– 不是所有学术方法都能直接应用

多角度思考– 当一条路走不通时，尝试其他途径

工具的价值– 好的工具能大大降低攻击难度

实事求是– 承认困难，寻找可行的替代方案

Deadpool: https://github.com/SideChannelMarvels/Deadpool

JeanGrey: https://github.com/SideChannelMarvels/JeanGrey

白盒密码学论文: Chow et al. (2002)


```
$ file WbaesWbaes: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, stripped$ ls -lh Wbaes-rwxr-xr-x 1 user user 9.3M Wbaes
```



```
$ ./Wbaes./wbaes plaintext$ ./Wbaes"aaaaaaaaaaaaaaaa"(无输出，退出码2)$ ./Wbaes"test"(无输出，退出码2)
```



```
$ strings Wbaes | grep -i"flag|success|correct"Here is flag{%s}
```



```
$ readelf -s Wbaes | grep FUNC 1: 08048260 0 FUNC GLOBAL DEFAULT UNDprintf@GLIBC_2.0 2: 08048270 0 FUNC GLOBAL DEFAULT UND memcpy@GLIBC_2.0 3: 08048280 0 FUNC GLOBAL DEFAULT UND memcmp@GLIBC_2.0 4: 08048290 0 FUNC GLOBAL DEFAULT UNDexit@GLIBC_2.0 5: 080482a0 0 FUNC GLOBAL DEFAULT UND strlen@GLIBC_2.0 6: 080482b0 0 FUNC GLOBAL DEFAULT UND sigaction@GLIBC_2.0
```



```
明文 → SubBytes(S盒) → ShiftRows → MixColumns → AddRoundKey(密钥) → 密文
```



```
明文 → T-Box1(包含S盒+密钥) → T-Box2 → ... → 密文
```



```
$ objdump -d Wbaes | head -100080482cc <.text>:80482cc: 89 25 80 a2 79 08 mov %esp,0x879a28080482d2: 8b 25 70 a2 79 08 mov 0x879a270,%esp80482d8: 8b a4 24 98 ff df ff mov -0x200068(%esp),%esp80482df: 8b a4 24 98 ff df ff mov -0x200068(%esp),%esp80482e6: 8b a4 24 98 ff df ff mov -0x200068(%esp),%esp...
```



```
add eax, ebx ; eax = eax + ebx
```



```
mov ecx, [lookup_table + eax*4] ; 查表mov edx, [lookup_table2 + ebx*4] ; 查表mov eax, [add_table + ecx + edx] ; 通过查表实现加法
```



```
┌─────────────────┐│ 接收命令行参数 ││ (16字节输入) │└────────┬────────┘ │ ▼┌─────────────────┐│ strlen检查长度 │ ───► 长度不对 ───► exit(1)│ (期望16字节) │└────────┬────────┘ │ ▼┌─────────────────┐│ 白盒AES加密 ││ (查找表计算) ││ MOV混淆执行 │└────────┬────────┘ │ ▼┌─────────────────┐│ memcmp比较结果 ││ 与预期密文比较 │└────────┬────────┘ │ ┌────┴────┐ │ │ 相同 不同 │ │ ▼ ▼┌────────┐ ┌─────┐│ printf │ │exit ││ flag │ │ (2) │└────────┘ └─────┘
```



```
第9轮输出 ─┬─► SubBytes ─► ShiftRows ─► AddRoundKey(K10) ─► 密文 │ 注入故障
```



```
正常密文: C = K10 ⊕ ShiftRows(SubBytes(S9))故障密文: C' = K10 ⊕ ShiftRows(SubBytes(S9'))差分: C ⊕ C' = ShiftRows(SubBytes(S9)) ⊕ ShiftRows(SubBytes(S9'))
```



```
K0 ──► K1 ──► K2 ──► ... ──► K10K0 ◄── K1 ◄── K2 ◄── ... ◄── K10 (可逆)
```



```
$ python3 dfa_attack.pyLvl 000 [0x10e0-0x1a2c[ nop 0x90 -> NoFaultLvl 000 [0x1a2c-0x2378[ nop 0x90 -> NoFault... 所有注入都是NoFault
```



```
$ python3 demo_complete_dfa.pyLvl 000 [0x28040-0xa7060[ nop 0x90 -> NoFault... 依然全部NoFault
```



```
fromCrypto.CipherimportAESkey =b'whctf&flappypig!'test_ciphertext = bytes.fromhex('683e34ced9b3ed089f841a2cf0e3924a')cipher = AES.new(key, AES.MODE_ECB)plaintext = cipher.decrypt(test_ciphertext)print(f"密钥:{key.decode()}")print(f"解密结果:{plaintext}")
```



```
密钥: whctf&flappypig!解密结果: b'testtesttesttest'
```



```
fromCrypto.CipherimportAESkey =b'whctf&flappypig!'cipher = AES.new(key, AES.MODE_ECB)# 读取二进制文件withopen('Wbaes','rb')asf: data = f.read()print(f"文件大小:{len(data)}字节")print("搜索可能的16字节密文...")# 遍历所有16字节块foriinrange(len(data) -15): block = data[i:i+16] try: plaintext = cipher.decrypt(block) # 检查解密结果是否包含可打印字符 printable_count = sum(1forbinplaintextif32<= b <127) ifprintable_count >=12: # 至少12个可打印字符 hex_str = block.hex() plain_str =''.join(chr(b)if32<= b <127else'.' forbinplaintext) print(f"n候选 @ 偏移 0x{i:08x}:") print(f" 密文:{hex_str}") print(f" 明文:{plaintext}") print(f" ASCII:{plain_str}") except: continue
```



```
$ python3 extract_ciphertext.py文件大小: 9770792 字节搜索可能的16字节密文...候选 @ 偏移 0x003a8162: 密文: 13cb006c2994de6da1b81ba399206290 明文: b'Whc7f&Fl@ppyp1g!' ASCII: Whc7f&Fl@ppyp1g!...
```



```
密文(hex): 13cb006c2994de6da1b81ba399206290明文: Whc7f&Fl@ppyp1g!
```



```
$ ./Wbaes"Whc7f&Fl@ppyp1g!"Here is flag{Whc7f&Fl@ppyp1g!}
```



```
fromCrypto.CipherimportAESimportsubprocesskey =b'whctf&flappypig!'flag =b'Whc7f&Fl@ppyp1g!'ciphertext = bytes.fromhex('13cb006c2994de6da1b81ba399206290')cipher = AES.new(key, AES.MODE_ECB)# 验证加密encrypted = cipher.encrypt(flag)print(f"加密验证:{encrypted.hex()}")print(f"期望密文:{ciphertext.hex()}")print(f"匹配:{encrypted == ciphertext}")# 验证解密decrypted = cipher.decrypt(ciphertext)print(f"解密验证:{decrypted}")print(f"匹配:{decrypted == flag}")# 运行程序result = subprocess.run(['./Wbaes', flag.decode()], capture_output=True, timeout=2)print(f"程序输出:{result.stdout.decode()}")
```



```
加密验证: 13cb006c2994de6da1b81ba399206290期望密文: 13cb006c2994de6da1b81ba399206290匹配: True解密验证: b'Whc7f&Fl@ppyp1g!'匹配: True程序输出: Here is flag{Whc7f&Fl@ppyp1g!}
```



```
# 文件类型识别file <binary># 字符串提取strings <binary># 符号表查看readelf -s <binary># 反汇编objdump -d <binary># 十六进制查看xxd <binary>
```



```
# PyCryptodome - AES加密fromCrypto.CipherimportAEScipher = AES.new(key, AES.MODE_ECB)encrypted = cipher.encrypt(plaintext)decrypted = cipher.decrypt(ciphertext)
```
