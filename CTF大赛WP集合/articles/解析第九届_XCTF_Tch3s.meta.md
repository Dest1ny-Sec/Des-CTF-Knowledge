---
title: 解析第九届 XCTF Tch3s
contest: XCTF 第九届
year: 2024
difficulty: medium
vuln_type: crypto_oracle
tags: [timing-attack, weak-PRNG, srand-time, seed-bruteforce, LD_PRELOAD, GDB-modify, AES-key-recover, side-channel]
attack_chain:
- 程序srand(time(NULL))初始化PRNG,16次rand()%256生成16字节key
- 加密flag输出密文后,进行多轮测试(随机明文加密+记录时间)
- 测试数据泄露随机数序列(明文就是rand()%256的输出)
- 遍历可能时间戳(~4000万值)作为候选seed
- 跳过16次rand()后生成16字节,与第一个测试明文匹配
- 找到正确seed后,LD_PRELOAD劫持srand设置SRAND环境变量
- GDB断点加密函数入口(0x30ba),写output密文到rdi缓冲区
- 直接调用解密函数(0x31a1),传入相同rdi/rsi/rdx参数
- 读取rsi缓冲区得flag
key_payload: XCTF{Tch3s_PRNG_...}
one_liner: 第九届XCTF Tch3s时序攻击+弱PRNG爆破,识别srand(time(NULL))弱种子+遍历时间戳匹配测试明文+LD_PRELOAD劫持+GDB调用解密函数。
lesson: srand(time(NULL))是经典弱PRNG,精度仅秒级,几分钟内可遍历几年;LD_PRELOAD劫持srand+GDB调用解密函数是经典的二进制复用技巧;侧信道信息泄露(测试明文)可作为种子恢复证据。
quality: high
---

## 题目列表

1道密码学:Tch3s 时序攻击+弱PRNG

## 关键考点

### 弱PRNG识别
- `srand(time(NULL))` 时间戳精度秒级
- 1秒内所有调用得到相同值
- 16次rand()%256生成16字节key

### 攻击原理
- 时间戳的可能范围有限(可估计程序运行时间)
- 几年的时间跨度只有约1亿可能值
- 现代计算机可在几分钟内暴力搜索

### 攻击步骤
1. 遍历可能时间戳作为种子
2. 对每个种子:
   - 调用srand(seed)
   - 跳过前16次rand()调用(密钥生成)
   - 生成16个随机数
   - 与第一个测试明文匹配
3. 找到匹配的种子后,重现密钥

### LD_PRELOAD劫持
```c
// my_srand.c
void srand(unsigned int seed) {
    seed = atoi(getenv("SRAND"));
    // 替换原始种子
}
```
- 编译:`gcc -shared -fPIC -o my_srand.so my_srand.c -ldl`
- 使用:`LD_PRELOAD=./my_srand.so SRAND=<找到的种子> ./Tch3s`

### GDB调用解密
- 加密函数地址:0x30ba(相对地址)
- 解密函数地址:0x31a1
- 断点加密函数入口
- 写output密文到rdi缓冲区
- 调用解密函数(0x31a1),传入相同rdi/rsi/rdx参数
- 读取rsi缓冲区得flag

### 经典案例
- 2008 OpenSSL Debian伪随机数漏洞(32768种可能)
- 2013 Android Bitcoin钱包SecureRandom缺陷ECDSA签名可预测
- 2010 PS3 ECDSA签名k重用导致私钥计算

## 实战价值
- 弱PRNG(srand(time)+单次rand)是CTF和实战的常见漏洞
- LD_PRELOAD劫持+环境变量传递是经典的二进制调试技巧
- GDB直接调用函数比重新实现解密逻辑更可靠
- 任何测试数据输出都可能泄露随机数序列
