---
title: 阿里云 CTF 2025 Writeup
contest: 阿里云CTF
year: 2025
difficulty: hard
vuln_type: misc_unknown
tags: [alibaba, BPF, verifier, eBPF, mmap, read-only-bypass, CUDA, PTX, AES, mba-overflow, kernel]
attack_chain:
  - 内核 bpf 扩展函数 alimem_mmap 把物理页 mmap 到用户空间实现零拷贝
  - bpf_func 接受 const 指针 1 与 const 指针 3，size=8，将 *ptr1 异或 2025 写 *ptr3
  - bpf verifier 在 LD 只读 map 时会预载入值，因此即便 pointer 3 实际指向 readonly map 也会通过校验
  - 内核执行时绕过 readonly 标记，实现只读内存写入 → 内核 RCE
  - 数学表达式侧：构造 99999999*(x^y) 12 次累加触发 64 位整数溢出
  - 表达式原值不等于溢出后值 → 绕过 expr!=expr 自检
  - RE 侧 dump PTX 提取 256 字节 S-box T 与逆表 RT，按 AES 标准逆出 flag
key_payload: '99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)'
one_liner: Alibaba CTF 2025 多方向题：eBPF 只读 map verifier 缺陷实现只读内存写入 RCE + mba 整数溢出绕自检 + CUDA PTX AES 逆向。
lesson: eBPF verifier 对只读 map 的预载入是经典绕过点（Map pre-load attack），用户空间的 mmap 物理页可被任意读写，配合 verifier 的提前优化形成只读页写洞。
quality: high
---

# 阿里云 CTF 2025 Writeup by Polaris 战队

**战队**: Polaris（第 12 名，2572 分）
**来源**: ctfiot.com ID 229002

## 一、内核 PWN（BPF）
### 漏洞点
- `alimem_mmap` 把物理页映射到用户空间，`bpf_func` 接受 `(const ptr1, size, const ptr3)`，把 `*ptr1` 异或 2025 后写入 `*ptr3`
- size 固定为 8
- 关键：**bpf verifier 对只读 map 做提前数据载入**——即便 ptr3 指向只读 map，verifier 看到 LD 指令时已"信任"这个值会预读取到栈/寄存器，运行时实际写入触发只读内存修改

### 攻击链
1. 用户态 `mmap` 一块物理页并以只读 map 的形式注册给 bpf 子系统
2. bpf prog 中调用 `BPF_LD_MAP_FD` 拿到只读 map 指针
3. `BPF_LDX_MEM(BPF_DW, ...)` 读取 map value 到 reg7（verifier 预读通过）
4. 调用扩展 `bpf_func` 把 reg7 异或 2025 后写回同一个 map value
5. 内核态无视 readonly 标记，写入完成 → 后续利用只读页被改的副作用实现 RCE

## 二、数学 mba 表达式溢出
### 约束
- 数字不超过 8 位
- 表达式长度 ≤ 200 字符
- 表达式项数 ≤ 15
- **表达式不能等于自己**

### 绕过
构造 `99999999*(x^y)` 12 次累加：
- 12×99999999 = 1199999988 < 2^31，但当 64 位溢出后值变化
- 原表达式 evaluate 与溢出后 evaluate 不等 → 满足"!=自己"约束
- 实际绕过是 z3/SAT 找溢出边界，让 `eval(before) != eval(after)`

## 三、easy-cuda-rev
### 解法
- IDA 跟踪 `cuda_encrypto` 找到注册 kernel `_Z14encrypt_kernelPhh`
- dump PTX（arch = sm_52, code version = [8,0]）
- 提取 `.const .align 1 .b8 T[256]` 256 字节 AES S-box
- 提取 `.const .align 1 .b8 RT[256]` 256 字节逆 S-box
- 字符串常量 `gift1:` `gift2:` `gift3:` `gift4:` `gift5:` 提示是 5 段分别加密
- 按 AES 标准流程逆出 5 段 flag

## 评价
Alibaba 2025 是高质量实战赛题：内核 eBPF 漏洞 + 数学 SAT + GPU 逆向，组合考察 kernel/PL/z3 多个深度方向。Polaris 战队排名 12 已是不错成绩。
