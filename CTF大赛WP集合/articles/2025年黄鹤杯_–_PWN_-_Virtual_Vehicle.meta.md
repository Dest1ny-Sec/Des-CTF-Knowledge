---
title: 2025 黄鹤杯 PWN Virtual_Vehicle（VM 逆向+VM PWN+seccomp）
contest: 2025 黄鹤杯
year: 2025
difficulty: hard
vuln_type: [vm, shellcode, rop, seccomp]
tags: [黄鹤杯 2025 PWN Virtual_Vehicle, 自定义 VM 逆向+VM PWN, vtable 8 个函数指针 (push_from_reg/push_from_imm/pop_to_reg/add_reg2_reg3_to_reg1/sub/mul/load/print), heap 0x1000 ope 字节码, hashtable mmap RWX 0x1000, seccomp-tools 沙箱, KILL execve, init_process() 初始化, main 9 种操作 8 种通过 vtable, 喷 shellcode 到 RWX]
attack_chain:
  - seccomp-tools 检查：禁 execve（KILL 0xc000003e != 0x3b），其他 ALLOW
  - 喷 shellcode 到 mmap 0x1000 RWX 段
  - main 9 种操作 → vtable 8 个函数指针
  - 字节码 choide (4字节) + arg (n*4字节)
  - 覆盖 vtable 指针或 hashtable 内容 → 控制流劫持
  - 9 种操作 + print_data 喷出 flag
  - 实际与车联网无关，是 VM 逆向+VM PWN
key_payload: "vtable 8 个函数指针 + hashtable RWX mmap 0x1000"
one_liner: 2025 黄鹤杯 PWN Virtual Vehicle：自定义 VM 字节码 + vtable 8 函数指针 + seccomp 禁 execve + hashtable RWX 段喷 shellcode。
lesson: VM PWN 套路：先反汇编字节码格式（choide+arg），再算 op 总数与 vtable 索引对应关系，seccomp-tools dump 是必做；本题实际是 VM 逆向（字节码 op）+ VM PWN（控制流劫持）混合。
quality: high
---

# 2025 黄鹤杯 PWN | Virtual_Vehicle

> 本题实际和车联网没什么关系，考察的是 VM 逆向和 VM PWN……主要是恶心。

## 勘察阶段

### seccomp 沙箱

```
line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x02 0xc000003e  if (A != ARCH_X86_64) goto 0004
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x15 0x00 0x01 0x0000003b  if (A != execve) goto 0005
 0004: 0x06 0x00 0x00 0x00000000  return KILL
 0005: 0x06 0x00 0x00 0x7fff0000  return ALLOW
```

禁 `execve` (0x3b)，其他 ALLOW → 走 ORW 拿 flag。

### init_process() 堆结构

```c
__int64 init_process() {
    vtable = malloc(0x40u);
    *(_QWORD *)vtable = push_from_reg;
    *((_QWORD *)vtable + 1) = push_from_imm;
    *((_QWORD *)vtable + 2) = pop_to_reg;
    *((_QWORD *)vtable + 3) = add_reg2_reg3_to_reg1;
    *((_QWORD *)vtable + 4) = sub_reg2_reg3_to_reg1;
    *((_QWORD *)vtable + 5) = mul_reg2_reg3_to_reg1;
    *((_QWORD *)vtable + 6) = load_data_from_reg;
    *((_QWORD *)vtable + 7) = print_data;
    
    heap = (unsigned int *)malloc(0x1000u);  // 字节码缓冲区
    hashtable = (unsigned int *)mmap(0, 0x1000u, 7, 34, -1, 0);  // RWX！喷 shellcode
    
    info = (struct Info *)malloc(0x30u);
    info->vtable = (void (*(*)[8])(...))vtable;
    info->offset = 0;
    info->stack_top = 0;
    info->stack_arena = heap;        // VM 栈
    info->register_arena = (unsigned int *)malloc(0x10u);  // 4 个寄存器
    info->data_arena = hashtable;    // 数据区（RWX）
    info->ope = (struct opcode *)malloc(0x1000u);  // 字节码
    
    return 0;
}
```

**vtable 8 个函数指针**：
1. push_from_reg
2. push_from_imm
3. pop_to_reg
4. add_reg2_reg3_to_reg1
5. sub_reg2_reg3_to_reg1
6. mul_reg2_reg3_to_reg1
7. load_data_from_reg
8. print_data

### main 9 种操作

```c
void __fastcall __noreturn main(int a1, char **a2, char **a3) {
    int n0x114514; // [rsp+14h] [rbp-Ch]
    signed int offset; // [rsp+18h] [rbp-8h]
    
    n0x114514 = 0;
    init_process();
    puts("Please input your op:");
    read(0, info->ope, 0x100u);
    
    while (1) {
        offset = info->offset;
        info->offset = offset + 5;
        switch (*(&info->ope->choide + offset)) {
            case 1: ((void (*)(QWORD))(*info->vtable)[0])((unsigned int)info->ope->arg[offset]); puts("op 0x1 executed"); break;
            case 2: ((void (*)(QWORD))(*info->vtable)[1])(*(unsigned int *)&info->ope->arg[offset]); puts("op 0x2 executed"); break;
            case 3: ((void (*)(QWORD))(*info->vtable)[2])((unsigned int)info->ope->arg[offset]); puts("op 0x3 executed"); break;
            case 4: (*info->vtable)[3]((unsigned int)info->ope->arg[offset], (unsigned int)info->ope->arg[offset+1], (unsigned int)info->ope->arg[offset+2]); puts("op 0x4 executed"); break;
            case 5: (*info->vtable)[4]((unsigned int)info->ope->arg[offset], (unsigned int)info->ope->arg[offset+1], (unsigned int)info->ope->arg[offset+2]); puts("op 0x5 executed"); break;
            ...
        }
    }
}
```

字节码格式：`choide (4 字节 op code) + arg (n*4 字节参数)`，每次 offset += 5（4+1 字节？）。

## 攻击思路

1. **喷 shellcode 到 hashtable**（mmap RWX 段）
2. **覆盖 vtable 指针**或 **load_data_from_reg 时跳到 hashtable**
3. **seccomp 禁 execve** → 走 ORW 拿 flag
4. **9 种 op + print_data 喷出 flag**
