---
title: 2024 年 KCTF 水泊梁山 - 反混淆
contest: KCTF大赛
year: 2024
difficulty: hard
vuln_type: [reverse, misc_unknown]
tags: [机器码特征码匹配, NOP 替换花指令, 线性扫描反汇编算法, Capstone 脚本, X64Dbg scylla dump, IDAPython ctree_visitor_t 删垃圾指令, pushf/popf + global var 化简, readeflags/writeeflags 删除, 全局变量 push ds: 还原]
attack_chain: 1. 机器码层特征匹配：9C FF 35 ?? ?? ?? ?? 8F 05 ?? ?? ?? ?? 9D 全部 NOP 替换 → X64Dbg scylla dump / 2. 线性扫描 + Capstone：识别 call imm + xor imm 还原基本块跳转 → jmp call 直接恢复 CFG / 3. IDAPython ctree_visitor_t 遍历 ctree 找 push ds:global + mov [esp], eax 模式 → nop + push eax / 4. readeflags/writeeflags 模式 cot_asg + cot_helper → 整行删
key_payload: findall "9C FF 35 ?? ?? ?? ?? 8F 05 ?? ?? ?? ?? 9D" ; memset 90 ; Scylla dump PE ; capstone Cs(CS_ARCH_X86, CS_MODE_32) 线性扫描 ; idaapi.ctree_visitor_t(CV_PARENTS) + isjunk(cot_asg + cot_helper)
one_liner: 机器码特征 NOP + Capstone 线性扫描 + IDAPython ctree 化简 + push eax 还原。
lesson: KCTF 反混淆标准流程：特征匹配 (第一遍) → CFG 还原 (第二遍) → 全局变量化简 (第三遍) → ctree AST 操作 (第四遍)。
quality: high
---
# 2024 KCTF 水泊梁山 - 反混淆

## 第一遍：机器码层特征匹配

```asm
;           pushf
;           jb      loc_3
;loc_1:     jmp     loc_2
;                   _ONE_BYTE_JUNKCODE_
;loc_2:     call    loc_4
;                   _TWO_BYTE_JUNKCODE_
;loc_3:     jb      loc_1
;                   _ONE_BYTE_JUNKCODE_
;loc_4:     add     esp,4
;           popf
;           jmp     loc_5
;                   _ONE_BYTE_JUNKCODE_
```

特征码：
```
S = 9C 72 0A EB 01 ?? E8 05 00 00 00 ?? ?? 72 F4 ?? 83 C4 04 9D EB 01 ??
R = 90 (NOP)
```

## 第二遍：IDAPython / Scylla dump

```python
# 用 Scylla plugin for x64dbg 提取 patch 后的程序
Dbg 停在 EP → Dump → PE Rebuild
```

## 第三遍：Capstone 线性扫描 + call imm 还原

```python
from capstone import *
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True

# 识别 call imm 模式：ret + push imm + push [mem] + xor imm
# callImm = (xor_imm ^ mem_dword) 是真实目标
scriptInsList.append(f"asm {hex(callImmKeyIns.address)},nop,1")
scriptInsList.append(f"asm {hex(ins.address)},nop,1")
scriptInsList.append(f"asm {hex(nextBlockIpIns.address)},call {hex(callImm)},1")
scriptInsList.append(f"asm {hex(callImmIns.address)},jmp {hex(nextBlockIp)},1")
```

`call imm` 四种类型分别处理：call imm / call [mem] / call reg / call [reg+offset]。

## 第四遍：ctree AST 化简（IDAPython）

```python
import idaapi, ida_hexrays
class JunkCodeVister(idaapi.ctree_visitor_t):
    def __init__(self, cfunc):
        idaapi.ctree_visitor_t.__init__(self, idaapi.CV_PARENTS)
        self.cfunc = cfunc
        self.del_point = 0
    def isjunk(self, ins):
        i = ins
        # __readeflags: v8 = __readeflags();
        if (i.op is idaapi.cit_expr and
            i.cexpr.op is idaapi.cot_asg and
            i.cexpr.x.op is idaapi.cot_var and
            i.cexpr.y.op is idaapi.cot_call and
            i.cexpr.y.x.op is idaapi.cot_helper):
            return True
        # __writeeflags: __writeeflags(v8);
        if (i.op is idaapi.cit_expr and
            i.cexpr.op is idaapi.cot_call and
            i.cexpr.x.op is idaapi.cot_helper and
            i.cexpr.a[0].op is idaapi.cot_var):
            return True
        return False
    def visit_insn(self, ins):
        if ins.op == idaapi.cit_if and self.del_point != 1:
            my_visitor = JunkCodeVister(self.cfunc)
            my_visitor.apply_to(ins, ins)
            self.prune_now()
            return 0
        if not ins.cexpr: return 0
        if self.isjunk(ins):
            pd = self.parent_insn().details
            dit = pd.find(ins)
            pd.erase(dit)
```

**目标模式**：
- `push dword ptr ds:[global_var]` + `mov [esp], eax` → nop + `push eax`
- 纯读全局变量（无运算）→ nop 删
- `readeflags/writeeflags` 对 → 整行删

## 全局变量化简

```python
GlobalVariantTable = {}
# 找 push ds:[global_var]
# 跟 200 条指令内是否参与运算
# 不参与 → 删 push/pop；参与 → 保留
```

**4 步还原链**：特征码匹配 → CFG 还原 → 全局变量化简 → ctree AST 删垃圾。
