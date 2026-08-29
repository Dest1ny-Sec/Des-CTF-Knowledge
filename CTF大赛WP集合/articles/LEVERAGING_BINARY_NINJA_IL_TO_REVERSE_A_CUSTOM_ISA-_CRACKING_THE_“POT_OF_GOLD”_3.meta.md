---
title: LEVERAGING BINARY NINJA IL TO REVERSE A CUSTOM ISA: CRACKING POT OF GOLD 37C3
contest: 37C3 (Chaos Communication Congress)
year: 2023
difficulty: hard
vuln_type: reverse
tags: [Binary Ninja, IL, custom ISA, unicorn_blob, 虚拟机, 字节码逆向]
attack_chain: |
  1. 题目: 37C3 (Chaos Communication Congress 2023) "Pot of Gold" — 逆向 unicorn_blob 格式 + 自定义 ISA 虚拟机
  2. unicorn_blob_file 结构:
     - magic[8] = "UNICORN"
     - nb_segments (uint16)
     - segments[nb_segments]: virtual_base + size + protection (1=read / 2=write / 4=exec)
     - data: 第一个 segment 数据
  3. 虚拟机结构:
     - regs[8]: 8 个 64-bit GPR
     - sp, lr, pc, fl (flags)
     - mem: 内存映射链表
     - handle_syscall, stopped, is_master
  4. exec_one_instruction 解析:
     - read_vm_memory(vm, pc, &opcode, 1) 读 1 字节 opcode
     - read_vm_memory(pc+1, &arg1, 1) 读 arg1
     - read_vm_memory(pc+2, &arg3, 1) + read_vm_memory(pc+3, &arg2, 1) → arg23 = _byteswap_ushort((arg3 << 8) | arg2)
  5. 指令集:
     - opcode 0: NOP
     - opcode 4: ALU (arg1>>4: 0=add, 1=sub, 2=mul, ...)
     - opcode 5: syscall (vm->handle_syscall(vm, arg1))
     - opcode 8: push (sp -= 8; write_vm_memory(sp, &regs[arg1], 8))
     - opcode 9: pop
     - opcode 0xC: ret (pc = lr)
  6. /chall /gordon.bin /tmp/x 1 & sleep 1; /chall /kitchen.bin /tmp/x 0: 同一 VM 跑两个 binary 共享 /tmp/x 通信
  7. Binary Ninja IL 分析: 把自定义 ISA lift 到 BNIL → 用 SSA 形式化分析数据流
  8. Python BinaryView 解析 unicorn_blob 格式 (.py 脚本恢复 IR)
key_payload: |
  # unicorn_blob_file:
  struct unicorn_blob_file {
    char magic[8];  // "UNICORN"
    uint16_t nb_segments;
    struct segment {
      uint16_t virtual_base;
      uint16_t size;
      uint16_t protection;  // 1=R, 2=W, 4=X
    } segments[nb_segments];
    char data[];
  };
  
  # VM:
  struct vm {
    uint64_t regs[8];
    uint64_t sp, lr, pc, fl;
    void *mem;
    void (*handle_syscall)(struct vm*, int);
    bool stopped, is_master;
  };
  
  # 指令格式 (4 字节):
  # opcode (1) | arg1 (1) | arg3 (1) | arg2 (1)
  # arg23 = _byteswap_ushort((arg3 << 8) | arg2)
  
  # BNIL 分析:
  from binaryninja.binaryview import BinaryView
  # 实现自定义 ISA 解析器 + IL lifting
one_liner: 37C3 2023 Pot of Gold: 用 Binary Ninja IL 逆向 unicorn_blob 格式 + 自定义 4 字节指令 ISA 虚拟机。
lesson: |
  - Binary Ninja IL (BNIL) 适合逆向自定义 ISA: 把字节码 lift 到 SSA 形式后用类型系统分析
  - unicorn_blob_file 是 37C3 出的标准格式: "UNICORN" magic + segments 表
  - 4 字节定长指令: opcode + 3 个 arg 字段，arg23 = byteswap((arg3<<8)|arg2)
  - 多 binary 共享 VM (/tmp/x IPC) 是隐藏通信通道
  - syscall 指令是逆向入口点: vm->handle_syscall(vm, syscall_id)
quality: high
---

# LEVERAGING BINARY NINJA IL TO REVERSE A CUSTOM ISA: CRACKING POT OF GOLD 37C3

> 来源: ctfiot.com 164127

## 题目格式 (unicorn_blob_file)

```c
struct unicorn_blob_file {
    char magic[8]; // const "UNICORN"
    uint16_t nb_segments;
    struct segment {
        uint16_t virtual_base;
        uint16_t size;
        uint16_t protection;  // bitfield: 1=R, 2=W, 4=X
    } segments[nb_segments];
    char data[ANYSIZE_ARRAY];  // 第一个 segment data
};
```

## 虚拟机结构

```c
struct vm {
    uint64_t regs[8];   // 8 GPR
    uint64_t sp;        // 栈指针
    uint64_t lr;        // 链接寄存器 (return address)
    uint64_t pc;        // 程序计数器
    uint64_t fl;        // 标志寄存器
    void *mem;          // 内存映射链表
    void (*handle_syscall)(struct vm*, int syscall_id);
    bool stopped;
    bool is_master;
};
```

## 指令集 (4 字节定长)

```c
int exec_one_instruction(vm *vm) {
    // 检查 PROT_EXEC 权限
    if ((get_segment_prot(vm, vm->pc) & PROT_EXEC) == 0) exit(1);
    
    // 读 4 字节指令
    read_vm_memory(vm, vm->pc, &opcode, 1);
    read_vm_memory(vm, vm->pc + 1, &arg1, 1);
    read_vm_memory(vm, vm->pc + 2, &arg3, 1);
    read_vm_memory(vm, vm->pc + 3, &arg2, 1);
    arg23 = _byteswap_ushort((arg3 << 8) | arg2);  // 大端转小端
    
    switch (opcode) {
        case 0:  // NOP
            break;
        case 4:  // ALU
            switch (arg1 >> 4) {
                case 0: vm->regs[arg3] = vm->regs[arg2] + operand; break;
                case 1: vm->regs[arg3] = vm->regs[arg2] - operand; break;
                case 2: vm->regs[arg3] = vm->regs[arg2] * operand; break;
                // ...
            }
            break;
        case 5:  // syscall
            vm->handle_syscall(vm, arg1);
            break;
        case 8:  // push
            vm->sp -= 8;
            write_vm_memory(vm, vm->sp, &vm->regs[arg1], 8);
            break;
        case 9:  // pop
            read_vm_memory(vm, vm->sp, &vm->regs[arg1], 8);
            vm->sp += 8;
            break;
        case 0xC:  // ret
            vm->pc = vm->lr;
            return 0;
    }
    vm->pc += 4;
}
```

## 隐藏通信通道

```sh
(/chall /gordon.bin /tmp/x 1 >/dev/null 2>/dev/null) &
sleep 1
/chall /kitchen.bin /tmp/x 0
```

`/chall` 跑两个 binary 共享 `/tmp/x` 文件作为 IPC 通道：gordon (master) + kitchen (slave) 通过 /tmp/x 通信。

## Binary Ninja IL 分析

```python
from struct import unpack
from binaryninja.binaryview import BinaryView
# 实现自定义 ISA 解析器
# 1. 解析 unicorn_blob_file 头
# 2. 把 segments 数据 lift 到 BNIL
# 3. 在 SSA 形式下分析数据流
```

## 评价

37C3 (Chaos Communication Congress) 2023 的"高级逆向"题：用 Binary Ninja IL 框架逆向自定义 ISA 虚拟机。

**亮点：**
- unicorn_blob 格式是 37C3 标准逆向格式
- 4 字节定长指令 + 大端/小端转换 (arg23 = byteswap)
- syscall 入口点是攻击面
- 多 binary 共享 /tmp/x IPC 是反调试隐蔽通信

**适用读者：** 逆向工程师 / Binary Ninja 高级用户 / 虚拟机逆向研究者
