---
title: 看雪2023 KCTF年度赛 | 第7题·智能联盟计划-设计思路及解析
contest: 看雪2023 KCTF年度赛
year: 2023
difficulty: hard
vuln_type: reverse
tags: [x86汇编混淆, keystone汇编+capstone反汇编, Python IDA脚本去混淆, 复杂混淆push eax/ebx模式, extract_block函数]
attack_chain: keystone.Ks(KS_ARCH_X86, KS_MODE_32)汇编+capstone反汇编→遍历ob_start到ob_end→识别混淆模式（push eax/ebx/ebx_ebp等标志）→extract_block提取真实指令→重建去混淆代码
key_payload: "keystone.Ks(KS_ARCH_X86, KS_MODE_32);capstone.Cs(CS_ARCH_X86, CS_MODE_32);ob_start=0x403AC0 ob_end=0x617DE0;extract_block提取真实指令;set_x86()"
one_liner: KCTF2023年度赛Q7《智能联盟计划》x86汇编混淆+keystone+capstone去混淆脚本
lesson: 大量x86混淆用keystone/capstone做汇编/反汇编引擎+Python遍历提取
quality: high
---

# 看雪2023 KCTF年度赛 | 第7题·智能联盟计划-设计思路及解析

**赛事**：看雪2023 KCTF年度赛 Q7《智能联盟计划》

**难度**：6队成功提交

**题目设计**：
- main函数未混淆（挺大）
- 其他函数都加了混淆
- 写脚本提取指令去混淆

**解析方法**：

**Step 1：分析混淆模式**
- 使用keystone做汇编、capstone做反汇编
- 遍历ob_start=0x403AC0到ob_end=0x617DE0的混淆代码
- 识别混淆flag：
  - `is_zero`（指令全为0）
  - `ebx_ebp`
  - `push_eax` / `push_ebx`
  - `eax_value` / `ebx_value`
  - `eax_value_2`
  - `push_eax_i` / `push_ebx_i`
  - `eax_value_i` / `eax_value_2_i`

**Step 2：去混淆脚本**：
```python
#!/usr/bin/env python3
# import ida_bytes
import keystone
import capstone

def set_x86():
    global ks, cs
    ks = keystone.Ks(keystone.ARCH_X86, keystone.MODE_32)
    cs = capstone.Cs(capstone.ARCH_X86, capstone.MODE_32)

set_x86()

def asm(code, addr=0):
    return bytes(ks.asm(code, addr)[0])

def disasm(code, addr=0):
    for i in cs.disasm(code, addr):
        return ('%s %s' % (i.mnemonic, i.op_str))

def ins_len(code):
    return len(next(cs.disasm(code, 0)).bytes)

def to_char(x):
    assert 0 <= x < 0x100
    if x >= 0x80: x -= 0x100
    return x

def to_int(b):
    assert len(b) == 4
    x = int.from_bytes(b, 'little')
    if x >= 1 << 31: x -= 1 << 32
    return x

def make_label(i):
    return '_%x' % (i + ob_start)

ob_start = 0x403AC0
ob_end = 0x617DE0
def extract_block(ins, i):
    is_zero = False
    ebx_ebp = False
    push_eax = False
    push_ebx = False
    # ... 多个flag组合判断
```

**核心技术**：
- 大量x86汇编混淆
- keystone / capstone 汇编-反汇编引擎
- Python脚本遍历ob_start-ob_end
- 多个flag组合识别（push eax/ebx等）
- extract_block提取真实指令

**质量评估**：高（去混淆Python脚本框架）
