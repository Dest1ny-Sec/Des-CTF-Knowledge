---
title: 解析2025强网拟态决赛easyre
contest: 强网拟态 2025 决赛 easyre
year: 2025
difficulty: medium
vuln_type: reverse
tags: [signal-handler, setjmp-longjmp, SIGSEGV, control-flow-obfuscation, TEA-decrypt, signal-based-vm, exception-based-cf, x86-pe32, 32-char-flag, wchar-key]
attack_chain:
- 文件:PE32+ x86-64 stripped to external PDB Windows 10 sections
- 关键字符串:Input flag / Wrong flag! Try again. / Success / Wrong length! Hint: 32 chars.
- 信号:SIGSEGV(11)访问违例+SIGILL非法指令+SIGFPE浮点异常+SIGINT中断
- 控制流混淆:
  1. signal(SIGSEGV, handler)注册信号处理函数
  2. setjmp保存当前执行上下文
  3. mov dword [0], eax触发SIGSEGV(向地址0写入)
  4. 操作系统捕获异常调用处理函数
  5. handler通过longjmp跳转回setjmp位置
- 正常控制流被异常处理打断,静态分析工具难跟踪
- 关键逻辑隐藏在异常处理函数中,不在主执行流
- TEA算法识别:
  - delta补码0x61C88647(标准TEA的delta补码)
  - sum初值=delta*32=0xC6EF3720
  - 位运算模式(左移4位+右移5位+异或+add+32轮)
  - Feistel结构(两个32位变量交替运算)
- 解密步骤:
  1. 检查signal函数导入
  2. 定位signal调用位置
  3. 识别异常触发点(向地址0写入)
  4. 找到异常处理函数
  5. 识别密钥读取位置
  6. 提取原始密钥数据+计算变换后的实际密钥
  7. 提取密文(8个32位整数=4组64位)
  8. 标准TEA解密
  9. 小端序转换ASCII字符(每4字节反转)
  10. 拼接得flag
key_payload: 0x9E3779B9 + 0x61C88647 + signal(SIGSEGV, handler)
one_liner: 强网拟态2025决赛easyre逆向,PE32+Windows+signal(SIGSEGV)+setjmp/longjmp控制流混淆+异常处理触发跳转+TEA解密(delta补码0x61C88647+sum初值0xC6EF3720+32轮Feistel+32字符flag)。
lesson: signal(SIGSEGV)+setjmp/longjmp是控制流混淆的经典手法;TEA特征常量0x9E3779B9+0xC6EF3720+0x61C88647快速识别;密钥常在异常处理函数中计算,需从handler提取。
quality: high
---

## 题目列表

1道Reverse:easyre(决赛)

## 关键考点

### 文件信息
- PE32+ executable (console) x86-64 (stripped to external PDB)
- for MS Windows, 10 sections
- 64位Windows可执行文件,已剥离调试符号

### 关键字符串
- "Input flag: " - 程序会要求用户输入
- "Wrong flag! Try again." - 输入错误的提示
- "Success! You got the flag." - 输入正确的提示
- "Wrong length! Hint: 32 chars." - 提示flag长度为32个字符

### 控制流混淆
```c
// 1. 注册异常处理函数
signal(SIGSEGV, handler);
// 2. 设置恢复点
setjmp(save_context);
// 3. 触发异常
mov dword [0], eax;  // 向地址0写入,触发SIGSEGV
// 4. 异常处理
// 操作系统捕获异常后,调用注册的处理函数
// 5. 恢复执行
handler通过longjmp跳转回setjmp保存的位置继续执行
```

### 信号列表
- SIGSEGV(信号值11):访问违例,通常由非法内存访问引起
- SIGILL:非法指令
- SIGFPE:浮点异常
- SIGINT:中断信号(如Ctrl+C)

### TEA算法特征
- 分组长度:64位(两个32位整数)
- 密钥长度:128位(四个32位整数)
- 轮数:32轮
- 结构:Feistel网络
- delta=0x9E3779B9(黄金分割比例*2^32)
- 解密时使用delta的补码:0x61C88647
- sum初值=delta*32=0xC6EF3720

### 特征识别
- 0x61C88647:这是TEA的delta值的补码
- 0xC6EF3720:delta*32的值,用于32轮迭代
- 位运算模式:典型的"左移4位"、"右移5位"、"异或"组合
- Feistel结构:两个32位变量交替运算
- 位移运算(扩散)+密钥混合(混淆)+累加运算(非线性)+XOR运算(可逆性)

### 解密步骤
1. 检查导入表,确认signal函数的导入
2. 定位signal函数的调用位置
3. 识别异常触发点(向地址0写入)
4. 找到异常处理函数的地址
5. 反汇编异常处理函数代码
6. 识别密钥读取位置
7. 理解密钥变换逻辑(XOR和SUB运算)
8. 提取原始密钥数据+计算变换后的实际密钥
9. 分析校验函数调用的加密函数
10. 寻找特征常量(0x61C88647, 0xC6EF3720)
11. 识别位运算模式
12. 确认32轮迭代循环
13. 通过比较逻辑找到密文存储位置
14. 使用工具提取密文数据
15. 实现标准TEA解密算法
16. 对8个32位整数(4组64位数据)进行解密
17. 小端序转换ASCII字符(每4字节反转)
18. 拼接得到完整flag

## 实战价值
- signal(SIGSEGV)+setjmp/longjmp是控制流混淆的经典手法
- TEA特征常量0x9E3779B9+0xC6EF3720+0x61C88647快速识别
- 密钥常在异常处理函数中计算,需从handler提取
- 静态分析时遇到大量跳转和混淆,黑盒+动态调试更高效
- 32字符flag长度是TEA的标准输入长度
