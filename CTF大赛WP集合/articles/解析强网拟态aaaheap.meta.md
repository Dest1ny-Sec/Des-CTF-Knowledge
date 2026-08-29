---
title: 解析强网拟态aaaheap
contest: 强网拟态 aaaheap
year: 2024
difficulty: hard
vuln_type: heap_exploit
tags: [arm64, aarch64, tcache, safe-linking, libc-leak, environ-leak, ROP, mprotect, malloc-hook, page-align-shift]
attack_chain:
- ARM64架构ELF aarch64,Full RELRO+NX+PIE+stripped
- tcache 7个块LIFO,fd指针单链表
- Safe-Linking保护:fd = (next_addr >> 12) ^ real_next(右移12位异或)
- 泄露堆地址→算加密值→修改fd指针为目标地址
- 分配到目标地址(控制chunk0指针)
- 读GOT表内容→计算libc base(atoi偏移)
- 读environ变量→定位栈地址
- 分配到栈,写入ROP链
- 触发执行,获得shell
- 关键寄存器:x0-x7参数/返回值,x8 syscall,x29 FP,x30 LR
- 内存页4KB右移12位相当于取页号
key_payload: aarch64 ROP + 栈劫持 + environ leak
one_liner: 强网拟态aaaheap ARM64架构下的tcache堆利用详解,涵盖Safe-Linking保护绕过(右移12位异或)+GOT泄露libc+environ泄露栈+栈分配+ROP劫持全流程。
lesson: ARM64堆利用与x86差异在寄存器约定(x0-x7参数/x8 syscall/x30 LR);Safe-Linking是glibc 2.32+的保护,需右移12位异或绕过;environ是定位栈地址的稳定向量。
quality: high
---

## 题目列表

1道PWN:ARM64 aaaheap

## 关键考点

### 题目环境
- 架构:ARM64 aarch64 64位
- 保护:Full RELRO / No Canary / NX / PIE / stripped
- libc 2.32+(safe-linking已启用)

### tcache基础
- 单线程最多7个块
- LIFO结构,fd单链表
- 64位:fd=8字节(实际是encrypted pointer)

### Safe-Linking保护
- glibc 2.32+引入
- fd = (next_addr >> 12) ^ real_next
- 内存页4KB=2^12,堆地址通常页对齐
- 右移12位相当于取页号
- 恢复:real_next = (current_addr >> 12) ^ stored_fd

### 攻击步骤
1. 分配两个堆块chunk0, chunk1
2. 释放chunk0到tcache
3. 已知堆地址(泄露或printk)
4. 计算加密值:crypt = (current_addr >> 12) ^ target_addr
5. 写入crypt覆盖chunk0的fd
6. 多次malloc分配到target_addr
7. 控制chunk0指针(任意地址读写)
8. 读GOT表内容→计算libc base
9. 读environ变量→定位栈地址
10. 分配到栈,写入ROP链
11. 触发执行,获得shell

### ARM64寄存器约定
- x0-x7:函数参数和返回值
- x8:系统调用号
- x29 (FP):帧指针
- x30 (LR):链接寄存器(存储返回地址)
- sp:栈指针

### 防护
- 释放后置NULL指针
- 使用智能指针(C++)
- 使用AddressSanitizer检测
- 缓解safe-linking:泄露堆地址才能计算加密值

## 实战价值
- ARM64架构在移动设备和嵌入式系统广泛应用
- Safe-Linking是glibc 2.32+必学保护
- environ定位栈地址是稳定向量
- ARM64 ROP与x86差异:x30 LR代替ret指令
- aarch64工具链:gdb-multiarch+pwntools+qemu-aarch64
