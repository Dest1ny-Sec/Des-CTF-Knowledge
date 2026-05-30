# Super Flagio CTF逆向题技术解析

> 原文: https://www.ctfiot.com/283888.html
> ID: 283888

Super Flagio CTF逆向题技术解析

题目概述

本题是一道基于cocos2d-x游戏引擎开发的Android逆向题目，附件为flagio.apk。这是一个模仿超级马里奥风格的游戏，玩家需要通过逆向分析找出正确的flag输入。

第一步：解压APK分析文件结构

首先使用unzip解压APK文件，查看其内部结构：

ounter(lineounter(linemkdir extracted && cd extractedunzip ../flagio.apk

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineextracted/├── assets/│ ├── res/ # 游戏资源文件（图片、音效）│ └── src/ # 加密的Lua脚本│ ├── 1024446525/│ ├── 1975478612/ # 包含核心检查逻辑│ │ └── 526018661 # checker脚本（1323字节）│ ├── 33309236/│ ├── 3914622949/│ └── 537350069├── lib/│ └── arm64-v8a/│ └── libgame.so # 游戏核心库（ARM64架构）├── classes.dex└── AndroidManifest.xml

cocos2d-x框架：assets/src目录下存放Lua脚本是cocos2d-x的典型特征

脚本加密：文件名是数字哈希而非.lua扩展名，说明经过混淆处理

64位架构：lib目录只有arm64-v8a，说明是64位应用

核心逻辑在Native层：libgame.so是主要分析目标

ounter(linestrings lib/arm64-v8a/libgame.so | grep -E "XXTEA|main.py|luajit|key"

ounter(lineounter(lineounter(lineounter(linemain.py./?.py;/usr/local/share/luajit-2.1.0-beta3/?.pyXXTEAxctf-flagio-2dx

LuaJIT 2.1.0-beta3：使用的Lua引擎版本，这决定了字节码格式

XXTEA：cocos2d-x框架常用的脚本加密算法

xctf-flagio-2dx：这是XXTEA加密的密钥

实现简单，代码量小

加解密速度快

安全性适中，足以防止简单的脚本窃取

ounter(linexxd assets/src/1975478612/526018661 | head -5

ounter(lineounter(line00000000: ffff dbee 6600 0000 1f22 412c 0000 000000000010: 8e0d 0000 4f28 1291 20b2 5ac3 fee5 0c51

字节0-1: 0xFFFF（签名标识）

字节2-5: 0xDBEE66（加密标志，表示使用XXTEA）

字节6+: 加密后的数据

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineAppDelegate::applicationDidFinishLaunching └─> LuaEngine::executeScriptFile("main.py") └─> LuaStack::executeScriptFile └─> FileUtils::getDataFromFile // 读取并解密文件 └─> XXTEA解密 └─> luaLoadBuffer // 加载解密后的字节码

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// hook luaLoadBuffer，第二个参数即为解密后的字节码Interceptor.attach(Module.findExportByName("libgame.so", "luaL_loadbuffer"), { onEnter: function(args) { var size = args[2].toInt32(); var bytecode = Memory.readByteArray(args[1], size); // 保存bytecode到文件 }});

opcode顺序被修改：标准LuaJIT的opcode顺序被重新排列

64位适配问题：需要处理LuaJIT64的双插槽机制

参照LuaJIT官方GitHub项目的src/vm_arm64.dasc汇编源码

在IDA中找到LuaJIT的dispatch table

逐个对照每条指令的处理函数

建立修改后的opcode与标准opcode的映射关系

重置opcode顺序映射表

适配LuaJIT64的双插槽机制（64位环境下某些常量占用两个槽位）

修改字节码解析逻辑

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineslot0.slot = { {}, -- slot[1]: 指令数组 {} -- slot[2]: 内存数组（256字节）}slot0.slot[3] = 0 -- 寄存器1slot0.slot[4] = 0 -- 寄存器2slot0.slot[5] = 1 -- 指令指针(IP)slot0.slot[6] = 0 -- 栈指针(SP)

slot[2][33-64]：用户输入的flag（32字节，对应ASCII字符）

slot[2][129-160]：预设的密文数组（32字节，用于验证）

slot[2][224-255]：加密后的结果存储区

ounter(lineounter(line[94, 106, 91, 110, 86, 100, 82, 20, 32, 20, 80, 21, 83, 107, 88, 98,81, 19, 79, 10, 49, 117, 68, 120, 61, 13, 75, 115, 48, 8, 76, 123]

Opcode

十进制

助记符

操作数

功能描述

0x11

17

INC_INPUT

n

input[n]++ 输入字节自增

0x12

18

DEC_INPUT

n

input[n]– 输入字节自减

0x21

33

INC_REG

r

reg[r-8]++ 寄存器自增

0x22

34

DEC_REG

r

reg[r-8]– 寄存器自减

0x23

35

XOR_IMM

r, imm

reg[r-8] ^= imm 与立即数异或

0x24

36

XOR_REG

r1, r2

reg[r1-8] ^= reg[r2-8] 寄存器间异或

0x25

37

POP_REG

r

reg[r-8] = pop() 弹栈到寄存器

0x31

49

POP_OUT

n

output[n] = pop() 弹栈到输出

0x32

50

PUSH_IN

n

push(input[n]) 输入压栈

0x41

65

PUSH_IMM

imm

push(imm) 立即数压栈

0x42

66

PUSH_REG

r

push(reg[r-8]) 寄存器压栈

0x90

144

RET

–

返回

ili函数：实现二进制异或运算（逐位比较）

lil函数：实现带溢出处理的加减运算

oOo函数：验证加密结果是否与预设密文匹配

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineinst = [65, 30, 37, 10, 50, 0, 37, 11, 36, 10, 11, 34, 10, 66, 10, 49, 0, ...]vm_ip = 0stack_ptr = 0while vm_ip < len(inst): opcode = inst[vm_ip] operand1 = inst[vm_ip + 1] if opcode == 0x41: # PUSH_IMM stack_ptr += 1 print(f"push({operand1}) // -> stack[{stack_ptr}]") vm_ip += 2 elif opcode == 0x25: # POP_REG print(f"reg{operand1 - 8} = pop() // stack[{stack_ptr}]") stack_ptr -= 1 vm_ip += 2 elif opcode == 0x32: # PUSH_IN stack_ptr += 1 print(f"push(input[{operand1}]) // -> stack[{stack_ptr}]") vm_ip += 2 elif opcode == 0x24: # XOR_REG operand2 = inst[vm_ip + 2] print(f"reg{operand1 - 8} ^= reg{operand2 - 8}") vm_ip += 3 elif opcode == 0x22: # DEC_REG print(f"reg{operand1 - 8}--") vm_ip += 2 elif opcode == 0x21: # INC_REG print(f"reg{operand1 - 8}++") vm_ip += 2 elif opcode == 0x42: # PUSH_REG stack_ptr += 1 print(f"push(reg{operand1 - 8}) // -> stack[{stack_ptr}]") vm_ip += 2 elif opcode == 0x31: # POP_OUT print(f"output[{operand1}] = pop() // stack[{stack_ptr}]") stack_ptr -= 1 vm_ip += 2 elif opcode == 0x90: # RET print("return") vm_ip += 1 else: break

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepush(30) // 常量30入栈reg2 = pop() // reg2 = 30push(input[0]) // 输入第一字节入栈reg3 = pop() // reg3 = input[0]reg2 ^= reg3 // reg2 = 30 ^ input[0]reg2-- // reg2 = (30 ^ input[0]) - 1push(reg2)output[0] = pop() // output[0] = (input[0] ^ 30) - 1

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepush(output[i-1]) // 前一个输出入栈reg2 = pop() // reg2 = output[i-1]push(input[i]) // 当前输入入栈reg3 = pop() // reg3 = input[i]reg2 ^= reg3 // reg2 = output[i-1] ^ input[i]reg2++ 或 reg2-- // 根据位置奇偶性决定push(reg2)output[i] = pop()

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linedef encrypt(plaintext): buf = list(plaintext) # 32字节输入 # 第一个字节：与常量30异或后减1 buf[0] = (buf[0] ^ 30) - 1 # 后续字节：链式加密 for i in range(1, 32): # 与前一个加密结果异或 buf[i] ^= buf[i - 1] # 根据位置进行加减操作 if i % 2 == 0 or i == 31: buf[i] -= 1 # 偶数位置和最后一位减1 else: buf[i] += 1 # 奇数位置加1 buf[i] &= 0xFF # 保持在字节范围内 return buf

链式依赖：每个输出字节依赖于前一个输出字节，形成加密链

异或混淆：使用XOR操作是对称加密的基础

奇偶差异处理：奇数和偶数位置采用不同的加减操作，增加复杂性

边界特殊处理：第一字节使用固定常量，最后一字节归类为”偶数”处理

任意一个字节的错误都会导致后续所有字节错误（雪崩效应）

无法单独破解某一位，必须从头开始

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#!/usr/bin/env python3"""Super Flagio CTF - Flag解密脚本"""# 密文数组（从反编译结果中提取）cipher = [94, 106, 91, 110, 86, 100, 82, 20, 32, 20, 80, 21, 83, 107, 88, 98, 81, 19, 79, 10, 49, 117, 68, 120, 61, 13, 75, 115, 48, 8, 76, 123]def decrypt(ciphertext): result = ciphertext.copy() # 关键：从后向前解密（逆序处理链式依赖） for i in range(31, 0, -1): # 逆向加减操作 if i % 2 == 0 or i == 31: result[i] = (result[i] + 1) & 0xFF # 原来-1，现在+1 else: result[i] = (result[i] - 1) & 0xFF # 原来+1，现在-1 # 逆向异或操作（与前一字节异或） result[i] ^= result[i - 1] # 第一字节的逆向处理 result[0] = ((result[0] + 1) ^ 30) & 0xFF return result# 执行解密decrypted = decrypt(cipher)flag = ''.join(chr(c) for c in decrypted)print(f"Flag: {flag}")

为什么要从后向前？

加密时buf[i]依赖buf[i-1]的加密结果

解密时需要用密文的buf[i-1]来还原buf[i]

从后向前可以保证每次使用的buf[i-1]都是原始密文值

逆运算关系

加密：+1 -> 解密：-1

加密：-1 -> 解密：+1

加密：XOR -> 解密：XOR（异或运算是自逆的）

第一字节特殊处理

加密：(input ^ 30) – 1 = cipher

解密：(cipher + 1) ^ 30 = input

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line密文数组:[94, 106, 91, 110, 86, 100, 82, 20, 32, 20, 80, 21, 83, 107, 88, 98,81, 19, 79, 10, 49, 117, 68, 120, 61, 13, 75, 115, 48, 8, 76, 123]解密结果（字节）:[65, 55, 54, 54, 57, 53, 55, 65, 53, 51, 69, 68, 65, 57, 50, 57,48, 67, 67, 70, 56, 69, 48, 51, 70, 49, 65, 57, 66, 55, 69, 48]Flag: A766957A53EDA9290CCF8E03F1A9B7E0验证成功！解密结果正确！

游戏界面有两排砖块，上排对应flag的前16个字符，下排对应后16个字符

玩家需要按照flag的顺序依次顶对应的砖块

输入正确后，顶问号块会出现蘑菇

吃掉蘑菇后碰板栗，墙壁消失

触碰旗帜完成通关

APK文件结构分析

Native库（.so文件）静态分析

字符串搜索和交叉引用

cocos2d-x框架架构理解

Lua脚本加载机制分析

XXTEA加密算法识别与破解

LuaJIT字节码格式理解

自定义opcode映射还原

反编译器修改适配64位

自定义VM架构逆向

指令集完整还原

执行流程模拟与跟踪

链式加密算法识别

逆向算法数学推导

解密脚本编写与验证

技术：XXTEA加密Lua脚本

目的：防止直接查看游戏逻辑

破解：提取密钥后解密

技术：修改LuaJIT opcode顺序

目的：阻止标准反编译器工作

破解：对照分析还原映射表

技术：核心算法用自定义VM实现

目的：增加逆向分析难度

破解：还原指令集并模拟执行

技术：JNI_OnLoad中包含检测

目的：阻止动态调试

破解：绕过或patch检测代码

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#!/usr/bin/env python3"""Super Flagio CTF - 完整解题脚本"""# 密文数组（从虚拟机分析中提取）cipher = [94, 106, 91, 110, 86, 100, 82, 20, 32, 20, 80, 21, 83, 107, 88, 98, 81, 19, 79, 10, 49, 117, 68, 120, 61, 13, 75, 115, 48, 8, 76, 123]# 从后向前解密for i in range(31, 0, -1): # 逆向加减操作 if i % 2 == 0 or i == 31: cipher[i] += 1 else: cipher[i] -= 1 cipher[i] &= 0xFF # 逆向异或操作 cipher[i] ^= cipher[i - 1]# 第一字节cipher[0] = (cipher[0] + 1) ^ 30# 输出结果flag = ''.join(chr(c) for c in cipher)print(flag)# A766957A53EDA9290CCF8E03F1A9B7E0


```
ounter(lineounter(linemkdir extracted && cd extractedunzip ../flagio.apk
```



```
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineextracted/├── assets/│ ├── res/ # 游戏资源文件（图片、音效）│ └── src/ # 加密的Lua脚本│ ├── 1024446525/│ ├── 1975478612/ # 包含核心检查逻辑│ │ └── 526018661 # checker脚本（1323字节）│ ├── 33309236/│ ├── 3914622949/│ └── 537350069├── lib/│ └── arm64-v8a/│ └── libgame.so # 游戏核心库（ARM64架构）├── classes.dex└── AndroidManifest.xml
```



```
ounter(linestrings lib/arm64-v8a/libgame.so | grep -E "XXTEA|main.py|luajit|key"
```



```
ounter(lineounter(lineounter(lineounter(linemain.py./?.py;/usr/local/share/luajit-2.1.0-beta3/?.pyXXTEAxctf-flagio-2dx
```



```
ounter(linexxd assets/src/1975478612/526018661 | head -5
```



```
ounter(lineounter(line00000000: ffff dbee 6600 0000 1f22 412c 0000 000000000010: 8e0d 0000 4f28 1291 20b2 5ac3 fee5 0c51
```



```
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineAppDelegate::applicationDidFinishLaunching └─> LuaEngine::executeScriptFile("main.py") └─> LuaStack::executeScriptFile └─> FileUtils::getDataFromFile // 读取并解密文件 └─> XXTEA解密 └─> luaLoadBuffer // 加载解密后的字节码
```



```
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// hook luaLoadBuffer，第二个参数即为解密后的字节码Interceptor.attach(Module.findExportByName("libgame.so", "luaL_loadbuffer"), { onEnter: function(args) { var size = args[2].toInt32(); var bytecode = Memory.readByteArray(args[1], size); // 保存bytecode到文件 }});
```



```
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineslot0.slot = { {}, -- slot[1]: 指令数组 {} -- slot[2]: 内存数组（256字节）}slot0.slot[3] = 0 -- 寄存器1slot0.slot[4] = 0 -- 寄存器2slot0.slot[5] = 1 -- 指令指针(IP)slot0.slot[6] = 0 -- 栈指针(SP)
```



```
ounter(lineounter(line[94, 106, 91, 110, 86, 100, 82, 20, 32, 20, 80, 21, 83, 107, 88, 98,81, 19, 79, 10, 49, 117, 68, 120, 61, 13, 75, 115, 48, 8, 76, 123]
```



```
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineinst = [65, 30, 37, 10, 50, 0, 37, 11, 36, 10, 11, 34, 10, 66, 10, 49, 0, ...]vm_ip = 0stack_ptr = 0while vm_ip < len(inst): opcode = inst[vm_ip] operand1 = inst[vm_ip + 1] if opcode == 0x41: # PUSH_IMM stack_ptr += 1 print(f"push({operand1}) // -> stack[{stack_ptr}]") vm_ip += 2 elif opcode == 0x25: # POP_REG print(f"reg{operand1 - 8} = pop() // stack[{stack_ptr}]") stack_ptr -= 1 vm_ip += 2 elif opcode == 0x32: # PUSH_IN stack_ptr += 1 print(f"push(input[{operand1}]) // -> stack[{stack_ptr}]") vm_ip += 2 elif opcode == 0x24: # XOR_REG operand2 = inst[vm_ip + 2] print(f"reg{operand1 - 8} ^= reg{operand2 - 8}") vm_ip += 3 elif opcode == 0x22: # DEC_REG print(f"reg{operand1 - 8}--") vm_ip += 2 elif opcode == 0x21: # INC_REG print(f"reg{operand1 - 8}++") vm_ip += 2 elif opcode == 0x42: # PUSH_REG stack_ptr += 1 print(f"push(reg{operand1 - 8}) // -> stack[{stack_ptr}]") vm_ip += 2 elif opcode == 0x31: # POP_OUT print(f"output[{operand1}] = pop() // stack[{stack_ptr}]") stack_ptr -= 1 vm_ip += 2 elif opcode == 0x90: # RET print("return") vm_ip += 1 else: break
```



```
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepush(30) // 常量30入栈reg2 = pop() // reg2 = 30push(input[0]) // 输入第一字节入栈reg3 = pop() // reg3 = input[0]reg2 ^= reg3 // reg2 = 30 ^ input[0]reg2-- // reg2 = (30 ^ input[0]) - 1push(reg2)output[0] = pop() // output[0] = (input[0] ^ 30) - 1
```



```
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepush(output[i-1]) // 前一个输出入栈reg2 = pop() // reg2 = output[i-1]push(input[i]) // 当前输入入栈reg3 = pop() // reg3 = input[i]reg2 ^= reg3 // reg2 = output[i-1] ^ input[i]reg2++ 或 reg2-- // 根据位置奇偶性决定push(reg2)output[i] = pop()
```



```
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linedef encrypt(plaintext): buf = list(plaintext) # 32字节输入 # 第一个字节：与常量30异或后减1 buf[0] = (buf[0] ^ 30) - 1 # 后续字节：链式加密 for i in range(1, 32): # 与前一个加密结果异或 buf[i] ^= buf[i - 1] # 根据位置进行加减操作 if i % 2 == 0 or i == 31: buf[i] -= 1 # 偶数位置和最后一位减1 else: buf[i] += 1 # 奇数位置加1 buf[i] &= 0xFF # 保持在字节范围内 return buf
```



```
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#!/usr/bin/env python3"""Super Flagio CTF - Flag解密脚本"""# 密文数组（从反编译结果中提取）cipher = [94, 106, 91, 110, 86, 100, 82, 20, 32, 20, 80, 21, 83, 107, 88, 98, 81, 19, 79, 10, 49, 117, 68, 120, 61, 13, 75, 115, 48, 8, 76, 123]def decrypt(ciphertext): result = ciphertext.copy() # 关键：从后向前解密（逆序处理链式依赖） for i in range(31, 0, -1): # 逆向加减操作 if i % 2 == 0 or i == 31: result[i] = (result[i] + 1) & 0xFF # 原来-1，现在+1 else: result[i] = (result[i] - 1) & 0xFF # 原来+1，现在-1 # 逆向异或操作（与前一字节异或） result[i] ^= result[i - 1] # 第一字节的逆向处理 result[0] = ((result[0] + 1) ^ 30) & 0xFF return result# 执行解密decrypted = decrypt(cipher)flag = ''.join(chr(c) for c in decrypted)print(f"Flag: {flag}")
```



```
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line密文数组:[94, 106, 91, 110, 86, 100, 82, 20, 32, 20, 80, 21, 83, 107, 88, 98,81, 19, 79, 10, 49, 117, 68, 120, 61, 13, 75, 115, 48, 8, 76, 123]解密结果（字节）:[65, 55, 54, 54, 57, 53, 55, 65, 53, 51, 69, 68, 65, 57, 50, 57,48, 67, 67, 70, 56, 69, 48, 51, 70, 49, 65, 57, 66, 55, 69, 48]Flag: A766957A53EDA9290CCF8E03F1A9B7E0验证成功！解密结果正确！
```



```
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#!/usr/bin/env python3"""Super Flagio CTF - 完整解题脚本"""# 密文数组（从虚拟机分析中提取）cipher = [94, 106, 91, 110, 86, 100, 82, 20, 32, 20, 80, 21, 83, 107, 88, 98, 81, 19, 79, 10, 49, 117, 68, 120, 61, 13, 75, 115, 48, 8, 76, 123]# 从后向前解密for i in range(31, 0, -1): # 逆向加减操作 if i % 2 == 0 or i == 31: cipher[i] += 1 else: cipher[i] -= 1 cipher[i] &= 0xFF # 逆向异或操作 cipher[i] ^= cipher[i - 1]# 第一字节cipher[0] = (cipher[0] + 1) ^ 30# 输出结果flag = ''.join(chr(c) for c in cipher)print(flag)# A766957A53EDA9290CCF8E03F1A9B7E0
```
