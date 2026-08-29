---
title: 解析2025强网拟态Icall
contest: 强网拟态 2025 Icall
year: 2025
difficulty: hard
vuln_type: reverse
tags: [anti-debug, prctl-tracer, proc-status, pthread-create, self-kill, custom-RC4, affine-cipher, prctl-bypass, GDB-return, multi-round]
attack_chain:
- ELF 64位 LSB, x86-64, dynamically linked, stripped
- 关键符号:pthread_create/prctl/getpid+kill
- 多线程反调试:
  - 主线程init阶段创建监控线程
  - 子线程prctl(PR_SET_PTRACER, ...)+读/proc/self/status检查TracerPid
  - TracerPid!=0 → kill自杀
- 绕反调试:GDB return命令直接跳过函数(动态) / Hook prctl系统调用 / 修改二进制NOP掉
- 三轮加密:r0uNd_Rc4(多轮RC4)+Aff1ne(仿射密码)+Enc1yp7(混淆名)
- 三轮循环次数:0x0C(12)+0x1E(30)+0x2A(42)
- 字符类型不同参数:
  - 数字0-9:模数10,乘数7,加数11,逆元3
  - 大写A-Z:模数26,乘数17,加数11,逆元15
  - 小写a-z:模数26,乘数17,加数11,逆元15
- 自定义S-box+多轮PRGA+CFB链式XOR
key_payload: r0uNd_Rc4 + Aff1ne + Enc1yp7
one_liner: 强网拟态2025 Icall多层加密+反调试对抗,pthread_create+prctl监控+TracerPid检测+kill自杀,绕反调试后三轮加密(多轮RC4+仿射+Enc1yp7)逐层解密。
lesson: 多线程反调试(子线程prctl+TracerPid检测)比单线程更难绕过;GDB的return命令是动态绕反调试最灵活的方法;多轮RC4+仿射+混淆函数名是常见组合加密模式。
quality: high
---

## 题目列表

1道Reverse:Icall多层加密+反调试

## 关键考点

### 文件信息
- ELF 64位 LSB, x86-64, dynamically linked, stripped
- 关键:.init_array段(初始化函数)+.data段(密文)+.rodata段(S-box)

### 多线程反调试
- 主线程init阶段创建监控子线程
- 子线程prctl(PR_SET_PTRACER, ...)设置跟踪权限
- 读取/proc/self/status检查TracerPid字段
- TracerPid!=0 → 正在被调试 → kill自杀

### 绕反调试三种方法
1. GDB的return命令直接跳过函数(动态,最灵活)
2. Hook prctl系统调用(LD_PRELOAD)
3. 修改二进制文件,NOP掉检测代码

### 三轮加密
- r0uNd_Rc4:多轮(Round)RC4加密
- Aff1ne:仿射(Affine)密码
- Enc1yp7:加密(Encrypt)的1337写法

### 加密参数表
- 数字0-9:模数(m)=10, 乘数(a)=7, 加数(b)=11, 逆元(a⁻¹)=3
- 大写A-Z:模数=26, 乘数=17, 加数=11, 逆元=15
- 小写a-z:模数=26, 乘数=17, 加数=11, 逆元=15

### RC4特征
- 自定义S-box初始值(256字节数组)
- 多轮PRGA生成单个密钥流字节
- CFB模式的链式XOR
- 三轮独立加密
- 模256运算+XOR操作
- 轮次循环次数:0x0C(12)+0x1E(30)+0x2A(42)

### 仿射密码
- 仿射变换:imul+add+idiv
- 验证互质性:gcd(a, m) = 1
- 计算乘法逆元(扩展欧几里得算法)
- 作为预处理层增加分析难度

### 三轮加密意义
- 多轮PRGA大幅增强密钥流随机性
- CFB模式消除相同明文的模式特征
- 三轮加密增加暴力破解复杂度

## 实战价值
- 多线程反调试(子线程prctl+TracerPid检测)比单线程更难绕过
- GDB的return命令是动态绕反调试最灵活的方法
- 多轮RC4+仿射+混淆函数名是常见组合加密模式
- 函数名混淆(r0uNd_Rc4/Aff1ne/Enc1yp7)是CTF逆向的常见手法
- CFB模式的链式XOR是流密码的稳定模式
