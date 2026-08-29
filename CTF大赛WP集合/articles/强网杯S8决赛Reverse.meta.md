---
title: 强网杯 S8 决赛 Reverse S1mpleVM
contest: 强网杯
year: 2024
difficulty: hard
vuln_type: reverse
tags: [custom-VM, stack-VM, LinkEntry, opcode-16, virtual-machine, compiler, vmrun, pwn-reverse]
attack_chain:
  - S1mpleVM 自定义栈式 VM，16 个 opcode
  - 数据结构: struct LinkEntry { signed val; LinkEntry *next; } 链表栈
  - case 0u: pop+pop+v7%v8 push 模运算（0x80000000 标志空栈）
  - case 1u: push PC+1 单字节
  - case 2u: pop to v5 (load)
  - case 3u: sub (类似)
  - case 4u: add
  - case 5u: bitwise NOT
  - case 6u: XOR
  - case 7u: OR
  - case 8u: AND
  - case 9u: CMP (类似)
  - case 10u: JMP PC
  - case 11u: JE
  - case 12u: JNE
  - case 13u: read (input)
  - case 14u: write (output)
  - case 15u: end
  - vmrun 接受 input + vmcode 字节码
  - 指令格式: 1 字节 opcode (vmcode[0]-16), 部分带 1 字节操作数 (vmcode[1])
key_payload: '16 opcode stack VM + LinkEntry 链表 + input/vmcode 参数'
one_liner: 强网杯 S8 决赛 S1mpleVM：自定义 16 opcode 栈式 VM 编译器，逆向需要还原指令语义。
lesson: 自定义 VM 逆向关键在数据结构（LinkEntry 链表栈）+ opcode 表 + 操作数格式（1 字节）。
quality: high
---

# 强网杯 S8 决赛 Reverse S1mpleVM

**来源**: ctfiot.com ID 220846

## VM 数据结构
```c
struct LinkEntry {
    signed int val;
    LinkEntry *next;
};
```

## VM 入口
```c
__int64 __fastcall vmrun(char *input, char *vmcode) {
    LinkEntry *v2 = NULL;  // 栈顶
    unsigned int opcode = *vmcode - 16;
    unsigned int v5;
    char *PC = vmcode + 1;
    while (1) {
        switch (opcode) {
            case 0u:  // MOD
                if (v2) {
                    int v7 = v2->val;
                    v2 = v2->next;
                    free(prev);
                    if (v2) {
                        int v8 = v2->val;
                        v2 = v2->next;
                        free(prev);
                    } else {
                        v8 = 0x80000000;  // 空栈标志
                    }
                } else {
                    v7 = 0x80000000;
                    v8 = 0x80000000;
                }
                v11 = malloc(0x10);
                v11->val = v7 % v8;
                v11->next = v2; v2 = v11;
                break;
            case 1u:  // PUSH
                v12 = *PC; v13 = malloc(0x10);
                v13->next = v2; v2 = v13; v13->val = v12;
                ++PC;
                break;
            case 2u:  // POP → v5
                if (v2) { v5 = v2->val; v2 = v2->next; free(v2); }
                else { v5 = 0x80000000; }
                break;
            // case 3u: SUB
            // case 4u: ADD
            // case 5u: NOT
            // case 6u: XOR
            // case 7u: OR
            // case 8u: AND
            // case 9u: CMP
            // case 10u: JMP
            // case 11u: JE
            // case 12u: JNE
            // case 13u: READ
            // case 14u: WRITE
            // case 15u: END
        }
    }
}
```

## 16 个 opcode（vmcode[0] - 16）

| opcode | 操作 | 说明 |
|--------|------|------|
| 0 | MOD | 弹 2 值做模运算，0x80000000 标志空栈 |
| 1 | PUSH imm8 | 压入 PC[1] 单字节立即数 |
| 2 | POP | 弹出到 v5 |
| 3 | SUB | 减法 |
| 4 | ADD | 加法 |
| 5 | NOT | 按位取反 |
| 6 | XOR | 异或 |
| 7 | OR | 或 |
| 8 | AND | 与 |
| 9 | CMP | 比较 |
| 10 | JMP | 跳转 |
| 11 | JE | 等于跳转 |
| 12 | JNE | 不等跳转 |
| 13 | READ | 读 input |
| 14 | WRITE | 写 output |
| 15 | END | 结束 |

## 评价
强网杯 S8 决赛 S1mpleVM 经典栈式 VM Reverse：
- 16 个 opcode 标准指令集
- 链表栈（malloc/free）
- 0x80000000 空栈标志
- 1 字节立即数操作数

是中级 VM 逆向标准训练题。
