---
title: 2023 上海磐石行动 WP - Polaris 战队
contest: 2023 上海磐石行动
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [keybox负数绕过, off_by_one, SROP, mprotect栈执行, mybash_structural_confusion, ret2dlresolve, RSA, RSA_repeated_squaring, Polaris战队]
attack_chain:
  - keybox: 负数数组下标绕过 s[v5]=v4 (v5=-9223372036854775796)
  - edit 负索引 (-0x398) 覆盖 v9 指针，调用 end 替代 exit
  - add(0x18) + edit(-0x398, 8, p64(0x401765)[:7]) 写 ROP
  - ssql: column off-by-one + 0x291 fake size + hijack 链表
  - libc 2.35 _IO_list_all + 0x52290 one_gadget
  - Hp: HTTP 自定义解析器 + off-by-one + 8 字节部分写
  - 改 chunk size 0x0101 + fake IO_FILE 触发 _IO_wfile_jumps
  - SROP: pop rax=10 + mprotect(rdi=stack, rsi=0x1000, rdx=7) + shellcode
  - mybash: realloc 调整 chunk_size + strncpy 类型混淆
  - ucontext_t SROP: rsp+0x100 控制 rip/rsp
  - changeaddr: 写 4 字节到 0x804C020 改 putchar GOT
  - RE ezEXE: switch case 反编译 + 数组字符串
  - encrytor: 反复跑 process 等 flag.txt.enc 含 flag
  - WEB ezpython: 模板注入
  - Crypto twice: getpq from e*d-1 + k=k//2 + gcd(powmod(g,k,n)-1, n) 分解
key_payload: 'first key = -9223372036854775796, second key = 1'
one_liner: 磐石行动 4 道 pwn：keybox 负数绕 + ssql 0x291+one_gadget + Hp SROP + mybash ucontext_t。
lesson: 负数数组下标可绕过 s[v5]=v4 边界；off-by-one + 0x291 fake size 是经典菜单题；ucontext_t SROP 在 realloc 场景里特别好用。
quality: high
---

# 2023 上海磐石行动 WP - Polaris 战队

## 来源
- 原文：ctfiot.com/119177.html
- 战队：Polaris（第四名）

## 5 道 pwn 详解

### 1. keybox（负数绕过）
```c
if (v5 > 2) exit(0);
s[v5] = v4;
if (s[12] == 1)  // 允许进入菜单
```
- first key = -9223372036854775796（绕过 v5 > 2 检查）
- second key = 1（写入 s[12]）
- edit(-0x398, 8, p64(0x401765)[:7]) 改 v9 指针指向 end
- end 不 exit 后续 ROP

### 2. ssql（off-by-one + fake size + one_gadget）
- 0x291 fake chunk size
- libc 2.35 `_IO_list_all` + 0x52290 one_gadget
- hijack0 链表 + 编辑 size + 触发 IO 攻击

### 3. Hp（HTTP parser + SROP）
- 自定义 HTTP 解析器
- off-by-one 改 size
- 8 字节部分写改 chunk metadata
- mprotect 栈为 RWX
- pop rax=10 + jmp rsp 跑 shellcode

### 4. mybash（realloc 调整 + ucontext_t SROP）
- echo + rm + cat 操作
- realloc 调整 chunk_size
- strncpy 类型混淆
- ucontext_t 拼 0x1c8 字节结构体
- 0x54f24 gadget + SROP 到 syscall 链

### 5. changeaddr（4 字节任意写）
- 0x804C020 改某 GOT 表
- 0x804932C 写值
- 触发段错误拿 flag

### RE
- **ezEXE**：switch case 0/1/2 返回 10/9/8，数组字符串多 flag
- **encrytor**：反复跑 process 等 flag.txt.enc 出现 flag

### WEB
- **ezpython**：模板注入（SSTI）

### Crypto
- **twice**：getpq from e*d-1 + k=k//2 + gcd(powmod(g,k,n)-1, n) 因子分解
  ```python
  def getpq(n, e, d):
      while True:
          k = e * d - 1
          g = random.randint(0, n)
          while k % 2 == 0:
              k = k // 2
              temp = gmpy2.powmod(g, k, n) - 1
              if gmpy2.gcd(temp, n) > 1 and temp != 0:
                  return gmpy2.gcd(temp, n)
  ```

## 关键技巧
- **负数下标绕过**：-9223372036854775796 当 64-bit signed 越界
- **off-by-one + 0x291 fake size**：菜单题经典堆攻击
- **ucontext_t SROP**：realloc 场景拼结构体
- **SROP + mprotect**：栈 RWX + pop rax=10 (mprotect) + syscall + jmp rsp
- **RSA getpq**：e*d-1 模 n-1 因子分解

## 适用场景
- 菜单 pwn 边界绕过
- libc 2.35 IO 攻击
- HTTP parser 漏洞
- shell bash 类型混淆
- 4 字节任意写
