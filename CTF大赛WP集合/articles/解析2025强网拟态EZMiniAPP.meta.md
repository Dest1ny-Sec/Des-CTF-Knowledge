---
title: 解析2025强网拟态EZMiniAPP
contest: 强网拟态 2025 EZMiniAPP
year: 2025
difficulty: medium
vuln_type: reverse
tags: [wechat-mini-program, wxapkg, big-endian, struct-unpack, XoR, rotl, enigmaticTransformation, js-decompile, mobile-reverse, crypto-identification]
attack_chain:
- 微信小程序:__APP__.wxapkg文件
- 二进制格式,包含JS代码+页面模板+样式表+配置文件
- wxapkg文件结构:文件头+索引区+数据区
- 解析:struct.unpack('B', data)解包1字节,struct.unpack('>I', data)解包4字节大端
- 文件名:UTF-8编码
- 加密函数:enigmaticTransformation(混淆名)
- 密钥:newKey2025!
- 预期密文:[1, 33, 194, 133, 195, 102, 232, 104, 200, 14, 8, 163, 131, 71, 68, 97, 2, 76, 72, 171, 74, 106, 225, 1, 65]
- 异或:交换律/结合律/自反性A^B^B=A/恒等律A^0=A/归零律A^A=0
- 循环左移(rotl)逆运算是循环右移(ror)
- 异或的逆运算仍是异或
- 解密:简化位运算表达式→识别算法类型(对称/非对称)→提取密钥→推导逆运算→实现解密
key_payload: enigmaticTransformation + newKey2025!
one_liner: 强网拟态2025 EZMiniAPP微信小程序逆向,wxapkg解包(二进制格式+大端索引+UTF-8文件名)+enigmaticTransformation加密函数+XOR/rotl逆运算推导+密钥newKey2025!。
lesson: 微信小程序逆向从__APP__.wxapkg开始,用unwxapkg/wxappUnpacker解包;JS代码混淆名(enigmaticTransformation)是常见模式;位运算加密(XOR/rotl)识别后逆运算就是它本身。
quality: medium
---

## 题目列表

1道Mobile:微信小程序逆向

## 关键考点

### 微信小程序格式
- .wxapkg是微信小程序的打包文件
- 特点:二进制格式,包含JS代码+页面模板+样式表+配置文件
- 文件结构:文件头+索引区+数据区
- 多字节整数使用大端序(Big-Endian)存储
- 文件偏移量是从wxapkg文件开头计算的绝对位置
- 文件名是UTF-8编码的字符串

### 解包工具
- unwxapkg (Python)
- wxappUnpacker (Node.js)
- struct.unpack('>I', data)解包4字节大端无符号整数

### 加密函数
- 函数名:enigmaticTransformation(混淆名)
- 密钥:newKey2025!
- 密文(预期):[1, 33, 194, 133, 195, 102, 232, 104, 200, 14, 8, 163, 131, 71, 68, 97, 2, 76, 72, 171, 74, 106, 225, 1, 65]

### XOR性质
- 交换律:A ^ B = B ^ A
- 结合律:(A ^ B) ^ C = A ^ (B ^ C)
- 自反性:A ^ B ^ B = A
- 恒等律:A ^ 0 = A
- 归零律:A ^ A = 0
- 加密和解密使用相同运算(对称性)

### 循环移位
- 循环左移(rotl)逆运算是循环右移(ror)
- 异或的逆运算仍是异或

### 解密步骤
1. 分析每个分支的实际计算结果
2. 简化位运算表达式
3. 找出运算的数学本质
4. 识别加密算法类型(对称/非对称)
5. 提取关键参数(密钥/IV/轮数)
6. 理解运算流程
7. 推导逆运算
8. 实现解密
9. 验证结果

## 实战价值
- 微信小程序逆向从__APP__.wxapkg开始
- unwxapkg/wxappUnpacker是解包必备工具
- JS代码混淆名(enigmaticTransformation)是常见模式
- 位运算加密(XOR/rotl)识别后逆运算就是它本身
- struct.unpack('>I', ...)大端是网络字节序标准
