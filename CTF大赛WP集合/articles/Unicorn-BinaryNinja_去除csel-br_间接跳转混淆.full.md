---
title: Unicorn-BinaryNinja 去除 csel-br 间接跳转混淆
contest: 技术文章 (CSDN 转载)
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags:
- unicorn_engine
- binaryninja
- arm64_obfuscation
- csel_cset
- indirect_branch
- smc_emulation
- code_patch
- b_cond_pair
- reverse_advanced
attack_chain: BN 遍历所有指令找 csel/cset+br 间接跳转对 → Unicorn 模拟执行两次 (trueReg/falseReg 各一次) 收集寄存器 → 计算 trueDest/falseDest → 验证是否在 text 段范围内 → 构造 b.cond 互补指令对 (b.eq/b.ne) → bv.write 覆盖原指令
key_payload: 'Architecture[''aarch64''].assemble("b.eq #0x123") / uc.emu_start(lastCsel[1]+4, curAddr) / ARM64_CONDS = {''eq'':''ne'',''ne'':''eq'',...}'
one_liner: 基于 Unicorn + BinaryNinja 的 ARM64 csel-br 间接跳转混淆自动化去除插件源码，逆向工程高级混淆的标配工具链。
lesson: 间接跳转混淆去除的核心是"分别模拟条件 true/false 两条路径"收集寄存器，确定 br Xn 的目标后用 b.cond 互补对替换。
quality: high
full_path: Unicorn-BinaryNinja_去除csel-br_间接跳转混淆.full.md
meta_path: Unicorn-BinaryNinja_去除csel-br_间接跳转混淆.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: Unicorn-BinaryNinja 去除 csel-br 间接跳转混淆。基于 Unicorn + BinaryNinja 的 ARM64 csel-br 间接跳转混淆自动化去除插件源码，逆向工程高级混淆的标配工具链。。经验：间接跳转混淆去除的核心是"分别模拟条件 true/false 两条路径"收集寄存器，确定 br Xn 的目标后用 b...
category: misc
subcategory: misc_other
tools_used:
- BinaryNinja
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/262287.html
reasoning_chain:
- 触发点：ARM64 反汇编遇到 csel/cset + br Xn 间接跳转对 → 反 IDA/反编译器无法解析目标
- '假设：csel/cset 提供 destReg = (cond) ? trueReg : falseReg 的条件赋值 → br 跳转目标由 destReg 决定'
- 动作：用 Unicorn Engine 在两条路径分别模拟执行，初始化 regs = emuToGetRegInitState(start, lastCsel[1]) 拿进入 csel 前的寄存器快照
- recover_regisers + uc.reg_write(destReg, regs[trueReg]) → emuToGetJumpReg(lastCsel[1]+4, curAddr) → trueDest
- recover_regisers + uc.reg_write(destReg, regs[falseReg]) → emuToGetJumpReg(lastCsel[1]+4, curAddr) → falseDest
- 观察：trueDest/falseDest 在 text 段范围内 → 假设：可生成 b.eq / b.ne 互补指令对 → 动作：buildOpAndPatch(bv, cond, trueDest, falseDest, curAddr)
- 'trueJmp = ''b.{} #{}''.format(cond, hex(trueDest-(curAddr-4))) / falseJmp = ''b.{} #{}''.format(ARM64_CONDS[cond], hex(falseDest-curAddr))'
- 动作：bv.write(curAddr-4, Architecture['aarch64'].assemble(trueJmp)) → 触发点：直接 patch 当前 br 指令前一条为 b.cond 真互补对
- 异常处理：UC_ERR_READ_UNMAPPED 时回溯到 preBB start，把 preBB.start 加入跳转白名单 white → workCsel 递归
- 蓝名单处理：避免BlHook hook 时把'bl'指令强制跳过白名单外的 bl 调用 → uc.reg_write(PC, address+4)
failed_attempts:
- 试图静态分析 csel 寄存器取值 → 失败：csel 前常有 add/sub 计算 brTarget，无法静态回推
- 试图单次模拟只算 trueDest → 失败：必须两次模拟分别填 trueReg / falseReg 拿到两条路径
- 试图在 x86 上跑同样思路 → 失败：ARM64 的 xzr/wzr 0 寄存器 Unicorn 不读，需手动赋 0
key_observations:
- 间接跳转混淆去除的核心是'分别模拟条件 true/false 两条路径'收集寄存器，确定 br Xn 的目标后用 b.cond 互补对替换
- Unicorn 模拟 ARM64 必须手动写 xzr/wzr 寄存器值，因 UC 不支持读 0 寄存器
- 递归处理 unmapped R/W 时回溯到 preBB start 加入跳转白名单是常见 workaround
- bv.write + Architecture['aarch64'].assemble 是 BinaryNinja Patch 标配 API
- ARM64_CONDS = {'eq':'ne','ne':'eq', ...} 互补对是 b.cond patch 必备
prerequisites:
- ARM64 汇编基础（csel/cset/br/b.cond 指令）
- Unicorn Engine API（Uc / mem_map / emu_start / reg_read / reg_write / hook_add）
- BinaryNinja Python API（bv.instructions / get_basic_blocks_at / write / get_disassembly）
- 插件开发基础（遍历指令 + 处理异常 + 递归）
- HOOK 编程（UC_HOOK_CODE + 跳转白名单）
---
# Unicorn-BinaryNinja 去除csel-br 间接跳转混淆

> 原文: https://www.ctfiot.com/262287.html
> ID: 262287

01

什么是间接跳转

02

如果我不会写自动化去除脚本怎么办？

CSET/CSEL是arm汇编中的两种条件赋值指令
CSEL的格式为  CESL dest source1 source2 cond
cond为条件标识，就是ge le eq之类的
当条件满足时dest会由source1赋值，否则由source2赋值
CSET的格式为  CSET dest cond
如果条件满足则dest被置1，否则置0

03

解决这个问题需要什么？

04

具体实现

uc = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
    uc.mem_map(CODE_BASE, CODE_SIZE, UC_PROT_ALL)  # 分配text段内存
    uc.mem_map(STACK_BASE, STACK_SIZE, UC_PROT_ALL)  # 分配栈内存
for segment in bv.segments:   # 用bn API遍历所有段
if segment.readable:
            start = segment.start
            end = segment.end
            size = end-start
print("[+] Mapping segment: [{}]".format(hex(segment.data_length)))
            content = bv.read(start, size)  # 读取段数据
            uc.mem_write(start, content)  # 写入uc模拟器

lastCsel = None
    lastCset = None
    nextWork = None   # 记录最后遇到的是csel还是cset
for instruction in bv.instructions: # 遍历所有指令
        curAddr = instruction[1]
# print(curAddr)
if instruction[0][0].text == "csel":
            lastCsel = instruction
            nextWork = "csel"
if instruction[0][0].text == "cset":
            lastCset = instruction
            nextWork = "cset"
if instruction[0][0].text == "br":
            tags = bv.get_functions_containing(curAddr)[0].tags # 获取当前函数的所有tag
            curTag = None
for tag in tags:
if tag[1] == curAddr:  #寻找br指令上的tag
                    curTag = tag[2]
break
if curTag is None or not (curTag.type.name == "Unresolved Indirect Control Flow"): # 查看是否为间接控制流
continue
# print(hex(curAddr))
            curBB = bv.get_basic_blocks_at(curAddr)[0]   # 获取当前指令所在的基本块
            curFunc = bv.get_functions_containing(curAddr)[0] # 获取当前指令所在的函数
# print(curBB)
if nextWork is None:
continue
try:
if nextWork == "csel":
if lastCsel[1] < curFunc.start or lastCsel[1] > curBB.end:  # 判断csel指令是否在当前函数内
continue
                    workCsel(uc, bv, lastCsel, instruction,
                             (curBB.start, curBB.end), (0xf4c0, 0x591d0), white=[curBB.start])
                    nextWork = None
elif nextWork == "cset": 
if lastCset[1] < curFunc.start or lastCset[1] > curBB.end: # 判断cset指令是否在当前函数内
continue
                    workCset(uc, bv, lastCset, instruction,
                             (curBB.start, curBB.end), (0xf4c0, 0x591d0), white=[curBB.start])
                    nextWork = None
except Exception as e: #  捕获预期外的异常
print("[{}] Error: {}".format(
hex(uc.reg_read(UC_ARM64_REG_PC)), e))

def workCsel(uc: Uc, bv: BinaryView, lastCsel: list, Brinstruction: list, emuRange: Tuple, textSecRange: Tuple, white: list = [], depth: int = 0)

Hook = uc.hook_add(UC_HOOK_CODE, avoidBlHook,
                           {"bv": bv, "white": white})
print(lastCsel)
print("[+] work at {} -- {}".format(hex(emuRange[0]), hex(emuRange[1])))
print("[+] cur search depth: {}".format(depth))

def avoidBlHook(uc: Uc, address, size, user_data):
    bv = user_data.get("bv")
    white = user_data.get("white")  # 把传过来的白名单和bv取出来
assert isinstance(bv, BinaryView)  # 不这样写编辑器不识别bv的类型
    code = bv.get_disassembly(address)  # 获取当前地址的指令
if "bl" in code:
for tar in white:
if hex(tar) in code:
if debugMode:
print("enter {}".format(hex(tar)))
break
else:  # 遍历白名单，如果遍历完都没有break，说明当前指令要被跳过
if debugMode:
print("[not {}] [skip {}] {}".format(
list(map(hex, white)), hex(address), code))
            uc.reg_write(UC_ARM64_REG_PC, address+4)  # 把pc设置为pc+4
if "b." in code:
for tar in white:
if hex(tar) in code:
if debugMode:
print("force jmp {}".format(hex(tar)))
# 这里如果遇到了白名单中的地址，直接把pc覆写成这个地址，即强制跳转
                uc.reg_write(UC_ARM64_REG_PC, tar)
break
else:
if debugMode:
print("skip unknown jmp target")
            uc.reg_write(UC_ARM64_REG_PC, address+4)  # 否则就跳过（不然也可能会被导到不知道哪里去）

def save_regisers(uc: Uc):
    regs = {}
for reg in ARM64_REG_MAP:
if ARM64_REG_MAP[reg] is not None:
            regs[reg] = uc.reg_read(ARM64_REG_MAP[reg]) # 读取所有寄存器信息并储存
return regs

def emuToGetRegInitState(uc: Uc, start: int, end: int) -> dict:
    stack_top = STACK_BASE + STACK_SIZE - 0x100
    uc.reg_write(UC_ARM64_REG_SP, stack_top)  # 设置栈指针
# 根据arm调用约定，初始的栈顶必须写8个0x00
    uc.mem_write(stack_top, b"x00x00x00x00x00x00x00x00")
    uc.emu_start(start, end)  # 开启模拟
return save_regisers(uc)

regs = emuToGetRegInitState(uc, emuRange[0], lastCsel[1])
# 获取进入CSEL之前的寄存器状态
# 然后因为CSEL的赋值选择第一个还是第二个参数是和cond对应的，br跳转必然前面跟一个add类的计算指令来计算地址
# 也就是说，这里提供了两条指令的空间来让我们构造一对互补的b.cond ，于是就规避了可能误修改业务相关指令的麻烦

        destReg = lastCsel[0][2].text
        trueReg = lastCsel[0][5].text
        falseReg = lastCsel[0][8].text
        cond = lastCsel[0][11].text
        brTarget = Brinstruction[0][2].text
        curAddr = Brinstruction[1]
# 这里搜集一些指令的参数信息，具体为什么这么写因为bn的指令token就是这么约定的

def emuToGetJumpReg(uc: Uc, start: int, end: int, brTarget: str) -> int:
    uc.emu_start(start, end)
    return uc.reg_read(ARM64_REG_MAP[brTarget])

def recover_regisers(uc: Uc, regs: dict):
    for reg in ARM64_REG_MAP:
        if ARM64_REG_MAP[reg] is not None:
            uc.reg_write(ARM64_REG_MAP[reg], regs[reg])
            # print("{}  =   {}".format(reg, hex(regs[reg])))

recover_regisers(uc, regs)
if trueReg == "xzr" or trueReg == "wzr":  # 这个主要是处理uc不能读取arm的0寄存器的问题，我们要手动赋0
    uc.reg_write(ARM64_REG_MAP[destReg], 0)
else:
    uc.reg_write(ARM64_REG_MAP[destReg],
                     regs[trueReg])
   # print(regs[trueReg])
trueDest = emuToGetJumpReg(uc, lastCsel[1]+4, curAddr,  brTarget)

recover_regisers(uc, regs)
if falseReg == "xzr" or falseReg == "wzr":
    uc.reg_write(ARM64_REG_MAP[destReg], 0)
else:
    uc.reg_write(ARM64_REG_MAP[destReg],
                 regs[falseReg])
# print(regs[falseReg])
falseDest = emuToGetJumpReg(
uc, lastCsel[1]+4, curAddr, brTarget)
if debugMode:
print("[+]  if ture then to:{} n else to:{}".format(
hex(trueDest), hex(falseDest)))
# print("[asm to replace]{}n[asm to replace]{}".format(bv.get_disassembly(
# curAddr-4), bv.get_disassembly(curAddr)))
uc.hook_del(Hook) # 在工作都做完后记得要解除hook，不然重复hook就挂了

if not (textSecRange[0] <= trueDest <= textSecRange[1]) or not (textSecRange[0] <= falseDest <= textSecRange[1]):  # 检查地址是否在text段范围内
print("[x] wrong dest occured,try to fix")
# 如果没有前驱基本块，说明此时处于函数的第一个基本块，要去找该函数的交叉引用
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
        preBB = bv.get_basic_blocks_at(ref[0].address)[
0]  # 获取交叉引用所处的基本块
        white.append(preBB.start)  # 把基本块开头加入跳转白名单
else:
        preBB = bv.get_basic_blocks_at(
            emuRange[0])[0].incoming_edges[0].source  # 如果有前驱基本块，就获取它
        white.append(preBB.start)  # 把基本块开头加入跳转白名单
print("[x] try find missing arg at {}".format(preBB))
    workCsel(uc, bv, lastCsel, Brinstruction, (preBB.start,
             emuRange[1]), textSecRange, white=white, depth=depth+1) # 递归向前追溯
else:  # 如果正常就组装指令并patch
        buildOpAndPatch(bv, cond, trueDest, falseDest, curAddr)

except UcError as e: # 捕获到错误地址读写或其他错误行为
    uc.hook_del(Hook)
    if e.errno == UC_ERR_READ_UNMAPPED or e.errno == UC_ERR_WRITE_UNMAPPED:
print("[x] unmapped R/W occured,try to fix    [{}    {}]".format(hex(
            uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
    else:
print("[!!!] unhanddle error: {}   [{}    {}]".format(e, hex(
            uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
    if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
        ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
        preBB = bv.get_basic_blocks_at(ref[0].address)[0]
        white.append(preBB.start)
    else:
        preBB = bv.get_basic_blocks_at(
            emuRange[0])[0].incoming_edges[0].source
        white.append(preBB.start)
print("[x] try find missing arg at {}".format(preBB))
workCsel(uc, bv, lastCsel, Brinstruction, (preBB.start,
                                               emuRange[1]), textSecRange, white=white, depth=depth+1)

def workCsel(uc: Uc, bv: BinaryView, lastCsel: list, Brinstruction: list, emuRange: Tuple, textSecRange: Tuple, white: list = [], depth: int = 0):
try:
        Hook = uc.hook_add(UC_HOOK_CODE, avoidBlHook,
                           {"bv": bv, "white": white})
print(lastCsel)
print("[+] work at {} -- {}".format(hex(emuRange[0]), hex(emuRange[1])))
print("[+] cur search depth: {}".format(depth))
        regs = emuToGetRegInitState(uc, emuRange[0], lastCsel[1])
# 获取进入CSEL之前的寄存器状态
# 然后因为CSEL的赋值选择第一个还是第二个参数是和cond对应的，br跳转必然前面跟一个add类的计算指令来计算地址
# 也就是说，这里提供了两条指令的空间来让我们构造一对互补的b.cond ，于是就规避了可能误修改业务相关指令的麻烦

        destReg = lastCsel[0][2].text
        trueReg = lastCsel[0][5].text
        falseReg = lastCsel[0][8].text
        cond = lastCsel[0][11].text
        brTarget = Brinstruction[0][2].text
        curAddr = Brinstruction[1]
# 这里搜集一些指令的参数信息，具体为什么这么写因为bn的指令token就是这么约定的
# print(regs)
if debugMode:
print(destReg, trueReg, falseReg, cond, brTarget)

# hk = uc.hook_add(UC_HOOK_CODE, codeHook, {"bv": bv})

        recover_regisers(uc, regs)
if trueReg == "xzr" or trueReg == "wzr":  # 这个主要是处理uc不能读取arm的0寄存器的问题，我们要手动赋0
            uc.reg_write(ARM64_REG_MAP[destReg], 0)
else:
            uc.reg_write(ARM64_REG_MAP[destReg],
                         regs[trueReg])
# print(regs[trueReg])
        trueDest = emuToGetJumpReg(
            uc, lastCsel[1]+4, curAddr,  brTarget)

        recover_regisers(uc, regs)
if falseReg == "xzr" or falseReg == "wzr":
            uc.reg_write(ARM64_REG_MAP[destReg], 0)
else:
            uc.reg_write(ARM64_REG_MAP[destReg],
                         regs[falseReg])
# print(regs[falseReg])
        falseDest = emuToGetJumpReg(
            uc, lastCsel[1]+4, curAddr, brTarget)
if debugMode:
print("[+]  if ture then to:{} n else to:{}".format(
hex(trueDest), hex(falseDest)))
# print("[asm to replace]{}n[asm to replace]{}".format(bv.get_disassembly(
# curAddr-4), bv.get_disassembly(curAddr)))
        uc.hook_del(Hook)
if not (textSecRange[0] <= trueDest <= textSecRange[1]) or not (textSecRange[0] <= falseDest <= textSecRange[1]):  # 检查地址是否在text段范围内
print("[x] wrong dest occured,try to fix")
# 如果没有前驱基本块，说明此时处于函数的第一个基本块，要去找该函数的交叉引用
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
                ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
                preBB = bv.get_basic_blocks_at(ref[0].address)[
0]  # 获取交叉引用所处的基本块
                white.append(preBB.start)  # 把基本块开头加入跳转白名单
else:
                preBB = bv.get_basic_blocks_at(
                    emuRange[0])[0].incoming_edges[0].source  # 如果有前驱基本块，就获取它
                white.append(preBB.start)  # 把基本块开头加入跳转白名单
print("[x] try find missing arg at {}".format(preBB))
            workCsel(uc, bv, lastCsel, Brinstruction, (preBB.start,
                     emuRange[1]), textSecRange, white=white, depth=depth+1)
else:  # 如果正常就组装指令并patch
            buildOpAndPatch(bv, cond, trueDest, falseDest, curAddr)
except UcError as e: # 捕获到错误地址读写或其他错误行为
        uc.hook_del(Hook)
if e.errno == UC_ERR_READ_UNMAPPED or e.errno == UC_ERR_WRITE_UNMAPPED:
print("[x] unmapped R/W occured,try to fix    [{}    {}]".format(hex(
                uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
else:
print("[!!!] unhanddle error: {}   [{}    {}]".format(e, hex(
                uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
            ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
            preBB = bv.get_basic_blocks_at(ref[0].address)[0]
            white.append(preBB.start)
else:
            preBB = bv.get_basic_blocks_at(
                emuRange[0])[0].incoming_edges[0].source
            white.append(preBB.start)
print("[x] try find missing arg at {}".format(preBB))
        workCsel(uc, bv, lastCsel, Brinstruction, (preBB.start,
                                                   emuRange[1]), textSecRange, white=white, depth=depth+1)

def buildOpAndPatch(bv: binaryview, cond: str, trueDest: int, falseDest: int, curAddr: int):
    trueJmp = "b.{} #{}".format(cond, hex(trueDest-(curAddr-4)))
    falseJmp = "b.{} #{}".format(ARM64_CONDS[cond], hex(falseDest-curAddr))
print("[asm gen]{}  ->  {}".format(bv.get_disassembly(curAddr-4), trueJmp))
print("[asm gen]{}  ->  {}".format(bv.get_disassembly(curAddr), falseJmp))
    # 使用bn提供的指令转换api获得机械码
    bv.write(curAddr-4, Architecture['aarch64'].assemble(trueJmp))
    bv.write(curAddr, Architecture['aarch64'].assemble(falseJmp))
print("===================================================")

05

完整代码

from binaryninja import *
from unicorn import *
from unicorn.arm64_const import *

CODE_BASE = 0x0
CODE_SIZE = 0x1200000+0x1000
STACK_BASE = 0x30000000
STACK_SIZE = 0x8000

ARM64_REG_MAP = {
'x0': UC_ARM64_REG_X0, 'x1': UC_ARM64_REG_X1, 'x2': UC_ARM64_REG_X2, 'x3': UC_ARM64_REG_X3,
'x4': UC_ARM64_REG_X4, 'x5': UC_ARM64_REG_X5, 'x6': UC_ARM64_REG_X6, 'x7': UC_ARM64_REG_X7,
'x8': UC_ARM64_REG_X8, 'x9': UC_ARM64_REG_X9, 'x10': UC_ARM64_REG_X10, 'x11': UC_ARM64_REG_X11,
'x12': UC_ARM64_REG_X12, 'x13': UC_ARM64_REG_X13, 'x14': UC_ARM64_REG_X14, 'x15': UC_ARM64_REG_X15,
'x16': UC_ARM64_REG_X16, 'x17': UC_ARM64_REG_X17, 'x18': UC_ARM64_REG_X18, 'x19': UC_ARM64_REG_X19,
'x20': UC_ARM64_REG_X20, 'x21': UC_ARM64_REG_X21, 'x22': UC_ARM64_REG_X22, 'x23': UC_ARM64_REG_X23,
'x24': UC_ARM64_REG_X24, 'x25': UC_ARM64_REG_X25, 'x26': UC_ARM64_REG_X26, 'x27': UC_ARM64_REG_X27,
'x28': UC_ARM64_REG_X28, 'x29': UC_ARM64_REG_X29,
'x30': UC_ARM64_REG_X30,
'sp': UC_ARM64_REG_SP,
'w0': UC_ARM64_REG_X0, 'w1': UC_ARM64_REG_X1, 'w2': UC_ARM64_REG_X2, 'w3': UC_ARM64_REG_X3,
'w4': UC_ARM64_REG_X4, 'w5': UC_ARM64_REG_X5, 'w6': UC_ARM64_REG_X6, 'w7': UC_ARM64_REG_X7,
'w8': UC_ARM64_REG_X8, 'w9': UC_ARM64_REG_X9, 'w10': UC_ARM64_REG_X10, 'w11': UC_ARM64_REG_X11,
'w12': UC_ARM64_REG_X12, 'w13': UC_ARM64_REG_X13, 'w14': UC_ARM64_REG_X14, 'w15': UC_ARM64_REG_X15,
'w16': UC_ARM64_REG_X16, 'w17': UC_ARM64_REG_X17, 'w18': UC_ARM64_REG_X18, 'w19': UC_ARM64_REG_X19,
'w20': UC_ARM64_REG_X20, 'w21': UC_ARM64_REG_X21, 'w22': UC_ARM64_REG_X22, 'w23': UC_ARM64_REG_X23,
'w24': UC_ARM64_REG_X24, 'w25': UC_ARM64_REG_X25, 'w26': UC_ARM64_REG_X26, 'w27': UC_ARM64_REG_X27,
'w28': UC_ARM64_REG_X28,
'wzr': None,
'xzr': None,
}
# 每个条件码逻辑上对应的互补的条件
ARM64_CONDS = {
'eq': 'ne',
'ne': 'eq',
'hs': 'lo',
'lo': 'hs',
'mi': 'pl',
'pl': 'mi',
'vs': 'vc',
'vc': 'vs',
'hi': 'ls',
'ls': 'hi',
'ge': 'lt',
'lt': 'ge',
'gt': 'le',
'le': 'gt',
'cs': 'cc',
'cc': 'cs',
}

def save_regisers(uc: Uc):
    regs = {}
for reg in ARM64_REG_MAP:
if ARM64_REG_MAP[reg] is not None:
            regs[reg] = uc.reg_read(ARM64_REG_MAP[reg])  # 读取所有寄存器信息并储存
return regs

def codeHook(uc: Uc, address, size, user_data):
    bv = user_data.get("bv")
    code = bv.get_disassembly(address)
    assert isinstance(bv, BinaryView)
if address >= 0x021e5c and address <= 0x21e74:
print("[{}]{}".format(
hex(address), code))
if address >= 0x000355f0 and address <= 0x00035668:
print("[{}]{}".format(
hex(address), code))

def recover_regisers(uc: Uc, regs: dict):
for reg in ARM64_REG_MAP:
if ARM64_REG_MAP[reg] is not None:
            uc.reg_write(ARM64_REG_MAP[reg], regs[reg])
# print("{}  =   {}".format(reg, hex(regs[reg])))

def emuToGetRegInitState(uc: Uc, start: int, end: int) -> dict:
    stack_top = STACK_BASE + STACK_SIZE - 0x100
    uc.reg_write(UC_ARM64_REG_SP, stack_top)  # 设置栈指针
# 根据arm调用约定，初始的栈顶必须写8个0x00
    uc.mem_write(stack_top, b"x00x00x00x00x00x00x00x00")
    uc.emu_start(start, end)  # 开启模拟
return save_regisers(uc)

def emuToGetJumpReg(uc: Uc, start: int, end: int, brTarget: str) -> int:
    uc.emu_start(start, end)
return uc.reg_read(ARM64_REG_MAP[brTarget])

debugMode = 1

def avoidBlHook(uc: Uc, address, size, user_data):
    bv = user_data.get("bv")
    white = user_data.get("white")  # 把传过来的白名单和bv取出来
    assert isinstance(bv, BinaryView)  # 不这样写编辑器不识别bv的类型
    code = bv.get_disassembly(address)  # 获取当前地址的指令
if "bl" in code:
for tar in white:
if hex(tar) in code:
if debugMode:
print("enter {}".format(hex(tar)))
break
else:  # 遍历白名单，如果遍历完都没有break，说明当前指令要被跳过
if debugMode:
print("[not {}] [skip {}] {}".format(
list(map(hex, white)), hex(address), code))
            uc.reg_write(UC_ARM64_REG_PC, address+4)  # 把pc设置为pc+4
if "b." in code:
for tar in white:
if hex(tar) in code:
if debugMode:
print("force jmp {}".format(hex(tar)))
# 这里如果遇到了白名单中的地址，直接把pc覆写成这个地址，即强制跳转
                uc.reg_write(UC_ARM64_REG_PC, tar)
break
else:
if debugMode:
print("skip unknown jmp target")
            uc.reg_write(UC_ARM64_REG_PC, address+4)  # 否则就跳过（不然也可能会被导到不知道哪里去）
# input()

def buildOpAndPatch(bv: binaryview, cond: str, trueDest: int, falseDest: int, curAddr: int):
    trueJmp = "b.{} #{}".format(cond, hex(trueDest-(curAddr-4)))
    falseJmp = "b.{} #{}".format(ARM64_CONDS[cond], hex(falseDest-curAddr))
print("[asm gen]{}  ->  {}".format(bv.get_disassembly(curAddr-4), trueJmp))
print("[asm gen]{}  ->  {}".format(bv.get_disassembly(curAddr), falseJmp))
    bv.write(curAddr-4, Architecture['aarch64'].assemble(trueJmp))
    bv.write(curAddr, Architecture['aarch64'].assemble(falseJmp))
print("===================================================")

def workCsel(uc: Uc, bv: BinaryView, lastCsel: list, Brinstruction: list, emuRange: Tuple, textSecRange: Tuple, white: list = [], depth: int = 0):
try:
        Hook = uc.hook_add(UC_HOOK_CODE, avoidBlHook,
                           {"bv": bv, "white": white})
print(lastCsel)
print("[+] work at {} -- {}".format(hex(emuRange[0]), hex(emuRange[1])))
print("[+] cur search depth: {}".format(depth))
        regs = emuToGetRegInitState(uc, emuRange[0], lastCsel[1])
# 获取进入CSEL之前的寄存器状态
# 然后因为CSEL的赋值选择第一个还是第二个参数是和cond对应的，br跳转必然前面跟一个add类的计算指令来计算地址
# 也就是说，这里提供了两条指令的空间来让我们构造一对互补的b.cond ，于是就规避了可能误修改业务相关指令的麻烦

        destReg = lastCsel[0][2].text
        trueReg = lastCsel[0][5].text
        falseReg = lastCsel[0][8].text
        cond = lastCsel[0][11].text
        brTarget = Brinstruction[0][2].text
        curAddr = Brinstruction[1]
# 这里搜集一些指令的参数信息，具体为什么这么写因为bn的指令token就是这么约定的
# print(regs)
if debugMode:
print(destReg, trueReg, falseReg, cond, brTarget)

# hk = uc.hook_add(UC_HOOK_CODE, codeHook, {"bv": bv})

recover_regisers(uc, regs)
if trueReg == "xzr" or trueReg == "wzr":  # 这个主要是处理uc不能读取arm的0寄存器的问题，我们要手动赋0
            uc.reg_write(ARM64_REG_MAP[destReg], 0)
else:
            uc.reg_write(ARM64_REG_MAP[destReg],
                         regs[trueReg])
# print(regs[trueReg])
        trueDest = emuToGetJumpReg(
            uc, lastCsel[1]+4, curAddr,  brTarget)

recover_regisers(uc, regs)
if falseReg == "xzr" or falseReg == "wzr":
            uc.reg_write(ARM64_REG_MAP[destReg], 0)
else:
            uc.reg_write(ARM64_REG_MAP[destReg],
                         regs[falseReg])
# print(regs[falseReg])
        falseDest = emuToGetJumpReg(
            uc, lastCsel[1]+4, curAddr, brTarget)
if debugMode:
print("[+]  if ture then to:{} n else to:{}".format(
hex(trueDest), hex(falseDest)))
# print("[asm to replace]{}n[asm to replace]{}".format(bv.get_disassembly(
# curAddr-4), bv.get_disassembly(curAddr)))
        uc.hook_del(Hook)
if not (textSecRange[0] <= trueDest <= textSecRange[1]) or not (textSecRange[0] <= falseDest <= textSecRange[1]):  # 检查地址是否在text段范围内
print("[x] wrong dest occured,try to fix")
# 如果没有前驱基本块，说明此时处于函数的第一个基本块，要去找该函数的交叉引用
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
                ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
                preBB = bv.get_basic_blocks_at(ref[0].address)[
0]  # 获取交叉引用所处的基本块
                white.append(preBB.start)  # 把基本块开头加入跳转白名单
else:
                preBB = bv.get_basic_blocks_at(
                    emuRange[0])[0].incoming_edges[0].source  # 如果有前驱基本块，就获取它
                white.append(preBB.start)  # 把基本块开头加入跳转白名单
print("[x] try find missing arg at {}".format(preBB))
workCsel(uc, bv, lastCsel, Brinstruction, (preBB.start,
                     emuRange[1]), textSecRange, white=white, depth=depth+1)
else:  # 如果正常就组装指令并patch
buildOpAndPatch(bv, cond, trueDest, falseDest, curAddr)
    
except UcError as e: # 捕获到错误地址读写或其他错误行为
        uc.hook_del(Hook)
if e.errno == UC_ERR_READ_UNMAPPED or e.errno == UC_ERR_WRITE_UNMAPPED:
print("[x] unmapped R/W occured,try to fix    [{}    {}]".format(hex(
                uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
else:
print("[!!!] unhanddle error: {}   [{}    {}]".format(e, hex(
                uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
            ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
            preBB = bv.get_basic_blocks_at(ref[0].address)[0]
            white.append(preBB.start)
else:
            preBB = bv.get_basic_blocks_at(
                emuRange[0])[0].incoming_edges[0].source
            white.append(preBB.start)
print("[x] try find missing arg at {}".format(preBB))
workCsel(uc, bv, lastCsel, Brinstruction, (preBB.start,
                                                   emuRange[1]), textSecRange, white=white, depth=depth+1)

def workCset(uc: Uc, bv: BinaryView, lastCset: list, Brinstruction: list, emuRange: Tuple, textSecRange: Tuple, white: list = [], depth: int = 0):
try:
        Hook = uc.hook_add(UC_HOOK_CODE, avoidBlHook,
                           {"bv": bv, "white": white, "end": emuRange[1]})
print(lastCset)
print("[+] work at {} -- {}".format(hex(emuRange[0]), hex(emuRange[1])))
print("[+] cur search depth: {}".format(depth))
        regs = emuToGetRegInitState(uc, emuRange[0], lastCset[1])

        destReg = lastCset[0][2].text
        cond = lastCset[0][5].text
        brTarget = Brinstruction[0][2].text
        curAddr = Brinstruction[1]
if debugMode:
print(destReg, cond, brTarget)
recover_regisers(uc, regs)
        uc.reg_write(ARM64_REG_MAP[destReg], 1)
        trueDest = emuToGetJumpReg(
            uc, lastCset[1]+4, curAddr,  brTarget)
recover_regisers(uc, regs)
        uc.reg_write(ARM64_REG_MAP[destReg], 0)
        falseDest = emuToGetJumpReg(
            uc, lastCset[1]+4, curAddr, brTarget)
if debugMode:
print("[+]  if ture then to:{} n else to:{}".format(
hex(trueDest), hex(falseDest)))
# print("[asm to replace]{}n[asm to replace]{}".format(bv.get_disassembly(
#     curAddr-4), bv.get_disassembly(curAddr)))
        uc.hook_del(Hook)
if not (textSecRange[0] <= trueDest <= textSecRange[1]) or not (textSecRange[0] <= falseDest <= textSecRange[1]):
print("[x] wrong dest occured,try to fix")
print("incoming edges: {}".format(
                bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges))
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
                ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
                preBB = bv.get_basic_blocks_at(ref[0].address)[0]
                white.append(preBB.start)
else:
                preBB = bv.get_basic_blocks_at(
                    emuRange[0])[0].incoming_edges[0].source
                white.append(preBB.start)
print("[x] try find missing arg at {}".format(preBB))
workCset(uc, bv, lastCset, Brinstruction, (preBB.start,
                     emuRange[1]), textSecRange, white=white, depth=depth+1)
else:
buildOpAndPatch(bv, cond, trueDest, falseDest, curAddr)

    
except UcError as e:
        uc.hook_del(Hook)
if e.errno == UC_ERR_READ_UNMAPPED or e.errno == UC_ERR_WRITE_UNMAPPED:
print("[x] unmapped R/W occured,try to fix    [{}    {}]".format(hex(
                uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
else:
print("[!!!] unhanddle error: {}   [{}    {}]".format(e, hex(
                uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
            ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
            preBB = bv.get_basic_blocks_at(ref[0].address)[0]
            white.append(preBB.start)
else:
            preBB = bv.get_basic_blocks_at(
                emuRange[0])[0].incoming_edges[0].source
            white.append(preBB.start)
print("[x] try find missing arg at {}".format(preBB))
workCset(uc, bv, lastCset, Brinstruction, (preBB.start,
                                                   emuRange[1]), textSecRange, white=white, depth=depth+1)

def solve(bv: BinaryView):
    uc = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
    uc.mem_map(CODE_BASE, CODE_SIZE, UC_PROT_ALL)  # 分配text段内存
    uc.mem_map(STACK_BASE, STACK_SIZE, UC_PROT_ALL)  # 分配栈内存
for segment in bv.segments:   # 用bn API遍历所有段
if segment.readable:
            start = segment.start
            end = segment.end
            size = end-start
print("[+] Mapping segment: [{}]".format(hex(segment.data_length)))
            content = bv.read(start, size)  # 读取段数据
            uc.mem_write(start, content)  # 写入uc模拟器
    lastCsel = None
    lastCset = None
    nextWork = None   # 记录最后遇到的是csel还是cset
for instruction in bv.instructions:  # 遍历所有指令
        curAddr = instruction[1]
# print(curAddr)
if instruction[0][0].text == "csel":
            lastCsel = instruction
            nextWork = "csel"
if instruction[0][0].text == "cset":
            lastCset = instruction
            nextWork = "cset"
if instruction[0][0].text == "br":
            tags = bv.get_functions_containing(curAddr)[0].tags  # 获取当前函数的所有tag
            curTag = None
for tag in tags:
if tag[1] == curAddr:  # 寻找br指令上的tag
                    curTag = tag[2]
break
# 查看是否为间接控制流
if curTag is None or not (curTag.type.name == "Unresolved Indirect Control Flow"):
continue
# print(hex(curAddr))
            curBB = bv.get_basic_blocks_at(curAddr)[0]   # 获取当前指令所在的基本块
            curFunc = bv.get_functions_containing(curAddr)[0]  # 获取当前指令所在的函数
# print(curBB)
if nextWork is None:
continue
try:
if nextWork == "csel":
if lastCsel[1] < curFunc.start or lastCsel[1] > curBB.end:  # 判断csel指令是否在当前函数内
continue
workCsel(uc, bv, lastCsel, instruction,
                             (curBB.start, curBB.end), (0xf4c0, 0x591d0), white=[curBB.start])
                    nextWork = None
                elif nextWork == "cset":
if lastCset[1] < curFunc.start or lastCset[1] > curBB.end:  # 判断cset指令是否在当前函数内
continue
workCset(uc, bv, lastCset, instruction,
                             (curBB.start, curBB.end), (0xf4c0, 0x591d0), white=[curBB.start])
                    nextWork = None
            
except Exception as e:  # 捕获预期外的异常
print("[{}] Error: {}".format(
hex(uc.reg_read(UC_ARM64_REG_PC)), e))

solve(bv)

06

鸣谢

看雪ID：SGSGsama

https://bbs.kanxue.com/user-home-1017025.htm

*本文为看雪论坛优秀文章，由 SGSGsama 原创，转载请注明来自看雪社区

议题征集中！看雪·第九届安全开发者峰会

# 往期推荐

企业微信 – 白日梦之获取登录二维码

《深入理解计算机系统》Attack Lab 题解

CVE-2024-0582 内核提权详细分析

App之算法分析

关于Office 2000的50次限制的研究

球分享

球点赞

球在看

点击阅读原文查看更多


```
CSET/CSEL是arm汇编中的两种条件赋值指令
CSEL的格式为  CESL dest source1 source2 cond
cond为条件标识，就是ge le eq之类的
当条件满足时dest会由source1赋值，否则由source2赋值
CSET的格式为  CSET dest cond
如果条件满足则dest被置1，否则置0
uc = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
    uc.mem_map(CODE_BASE, CODE_SIZE, UC_PROT_ALL)  # 分配text段内存
    uc.mem_map(STACK_BASE, STACK_SIZE, UC_PROT_ALL)  # 分配栈内存
for segment in bv.segments:   # 用bn API遍历所有段
if segment.readable:
            start = segment.start
            end = segment.end
            size = end-start
print("[+] Mapping segment: [{}]".format(hex(segment.data_length)))
            content = bv.read(start, size)  # 读取段数据
            uc.mem_write(start, content)  # 写入uc模拟器
lastCsel = None
    lastCset = None
    nextWork = None   # 记录最后遇到的是csel还是cset
for instruction in bv.instructions: # 遍历所有指令
        curAddr = instruction[1]
# print(curAddr)
if instruction[0][0].text == "csel":
            lastCsel = instruction
            nextWork = "csel"
if instruction[0][0].text == "cset":
            lastCset = instruction
            nextWork = "cset"
if instruction[0][0].text == "br":
            tags = bv.get_functions_containing(curAddr)[0].tags # 获取当前函数的所有tag
            curTag = None
for tag in tags:
if tag[1] == curAddr:  #寻找br指令上的tag
                    curTag = tag[2]
break
if curTag is None or not (curTag.type.name == "Unresolved Indirect Control Flow"): # 查看是否为间接控制流
continue
# print(hex(curAddr))
            curBB = bv.get_basic_blocks_at(curAddr)[0]   # 获取当前指令所在的基本块
            curFunc = bv.get_functions_containing(curAddr)[0] # 获取当前指令所在的函数
# print(curBB)
if nextWork is None:
continue
try:
if nextWork == "csel":
if lastCsel[1] < curFunc.start or lastCsel[1] > curBB.end:  # 判断csel指令是否在当前函数内
continue
                    workCsel(uc, bv, lastCsel, instruction,
                             (curBB.start, curBB.end), (0xf4c0, 0x591d0), white=[curBB.start])
                    nextWork = None
elif nextWork == "cset": 
if lastCset[1] < curFunc.start or lastCset[1] > curBB.end: # 判断cset指令是否在当前函数内
continue
                    workCset(uc, bv, lastCset, instruction,
                             (curBB.start, curBB.end), (0xf4c0, 0x591d0), white=[curBB.start])
                    nextWork = None
except Exception as e: #  捕获预期外的异常
print("[{}] Error: {}".format(
hex(uc.reg_read(UC_ARM64_REG_PC)), e))
def workCsel(uc: Uc, bv: BinaryView, lastCsel: list, Brinstruction: list, emuRange: Tuple, textSecRange: Tuple, white: list = [], depth: int = 0)
Hook = uc.hook_add(UC_HOOK_CODE, avoidBlHook,
                           {"bv": bv, "white": white})
print(lastCsel)
print("[+] work at {} -- {}".format(hex(emuRange[0]), hex(emuRange[1])))
print("[+] cur search depth: {}".format(depth))
def avoidBlHook(uc: Uc, address, size, user_data):
    bv = user_data.get("bv")
    white = user_data.get("white")  # 把传过来的白名单和bv取出来
assert isinstance(bv, BinaryView)  # 不这样写编辑器不识别bv的类型
    code = bv.get_disassembly(address)  # 获取当前地址的指令
if "bl" in code:
for tar in white:
if hex(tar) in code:
if debugMode:
print("enter {}".format(hex(tar)))
break
else:  # 遍历白名单，如果遍历完都没有break，说明当前指令要被跳过
if debugMode:
print("[not {}] [skip {}] {}".format(
list(map(hex, white)), hex(address), code))
            uc.reg_write(UC_ARM64_REG_PC, address+4)  # 把pc设置为pc+4
if "b." in code:
for tar in white:
if hex(tar) in code:
if debugMode:
print("force jmp {}".format(hex(tar)))
# 这里如果遇到了白名单中的地址，直接把pc覆写成这个地址，即强制跳转
                uc.reg_write(UC_ARM64_REG_PC, tar)
break
else:
if debugMode:
print("skip unknown jmp target")
            uc.reg_write(UC_ARM64_REG_PC, address+4)  # 否则就跳过（不然也可能会被导到不知道哪里去）
def save_regisers(uc: Uc):
    regs = {}
for reg in ARM64_REG_MAP:
if ARM64_REG_MAP[reg] is not None:
            regs[reg] = uc.reg_read(ARM64_REG_MAP[reg]) # 读取所有寄存器信息并储存
return regs

def emuToGetRegInitState(uc: Uc, start: int, end: int) -> dict:
    stack_top = STACK_BASE + STACK_SIZE - 0x100
    uc.reg_write(UC_ARM64_REG_SP, stack_top)  # 设置栈指针
# 根据arm调用约定，初始的栈顶必须写8个0x00
    uc.mem_write(stack_top, b"x00x00x00x00x00x00x00x00")
    uc.emu_start(start, end)  # 开启模拟
return save_regisers(uc)

regs = emuToGetRegInitState(uc, emuRange[0], lastCsel[1])
# 获取进入CSEL之前的寄存器状态
# 然后因为CSEL的赋值选择第一个还是第二个参数是和cond对应的，br跳转必然前面跟一个add类的计算指令来计算地址
# 也就是说，这里提供了两条指令的空间来让我们构造一对互补的b.cond ，于是就规避了可能误修改业务相关指令的麻烦

        destReg = lastCsel[0][2].text
        trueReg = lastCsel[0][5].text
        falseReg = lastCsel[0][8].text
        cond = lastCsel[0][11].text
        brTarget = Brinstruction[0][2].text
        curAddr = Brinstruction[1]
# 这里搜集一些指令的参数信息，具体为什么这么写因为bn的指令token就是这么约定的
def emuToGetJumpReg(uc: Uc, start: int, end: int, brTarget: str) -> int:
    uc.emu_start(start, end)
    return uc.reg_read(ARM64_REG_MAP[brTarget])

def recover_regisers(uc: Uc, regs: dict):
    for reg in ARM64_REG_MAP:
        if ARM64_REG_MAP[reg] is not None:
            uc.reg_write(ARM64_REG_MAP[reg], regs[reg])
            # print("{}  =   {}".format(reg, hex(regs[reg])))

recover_regisers(uc, regs)
if trueReg == "xzr" or trueReg == "wzr":  # 这个主要是处理uc不能读取arm的0寄存器的问题，我们要手动赋0
    uc.reg_write(ARM64_REG_MAP[destReg], 0)
else:
    uc.reg_write(ARM64_REG_MAP[destReg],
                     regs[trueReg])
   # print(regs[trueReg])
trueDest = emuToGetJumpReg(uc, lastCsel[1]+4, curAddr,  brTarget)
recover_regisers(uc, regs)
if falseReg == "xzr" or falseReg == "wzr":
    uc.reg_write(ARM64_REG_MAP[destReg], 0)
else:
    uc.reg_write(ARM64_REG_MAP[destReg],
                 regs[falseReg])
# print(regs[falseReg])
falseDest = emuToGetJumpReg(
uc, lastCsel[1]+4, curAddr, brTarget)
if debugMode:
print("[+]  if ture then to:{} n else to:{}".format(
hex(trueDest), hex(falseDest)))
# print("[asm to replace]{}n[asm to replace]{}".format(bv.get_disassembly(
# curAddr-4), bv.get_disassembly(curAddr)))
uc.hook_del(Hook) # 在工作都做完后记得要解除hook，不然重复hook就挂了
if not (textSecRange[0] <= trueDest <= textSecRange[1]) or not (textSecRange[0] <= falseDest <= textSecRange[1]):  # 检查地址是否在text段范围内
print("[x] wrong dest occured,try to fix")
# 如果没有前驱基本块，说明此时处于函数的第一个基本块，要去找该函数的交叉引用
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
        preBB = bv.get_basic_blocks_at(ref[0].address)[
0]  # 获取交叉引用所处的基本块
        white.append(preBB.start)  # 把基本块开头加入跳转白名单
else:
        preBB = bv.get_basic_blocks_at(
            emuRange[0])[0].incoming_edges[0].source  # 如果有前驱基本块，就获取它
        white.append(preBB.start)  # 把基本块开头加入跳转白名单
print("[x] try find missing arg at {}".format(preBB))
    workCsel(uc, bv, lastCsel, Brinstruction, (preBB.start,
             emuRange[1]), textSecRange, white=white, depth=depth+1) # 递归向前追溯
else:  # 如果正常就组装指令并patch
        buildOpAndPatch(bv, cond, trueDest, falseDest, curAddr)
except UcError as e: # 捕获到错误地址读写或其他错误行为
    uc.hook_del(Hook)
    if e.errno == UC_ERR_READ_UNMAPPED or e.errno == UC_ERR_WRITE_UNMAPPED:
print("[x] unmapped R/W occured,try to fix    [{}    {}]".format(hex(
            uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
    else:
print("[!!!] unhanddle error: {}   [{}    {}]".format(e, hex(
            uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
    if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
        ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
        preBB = bv.get_basic_blocks_at(ref[0].address)[0]
        white.append(preBB.start)
    else:
        preBB = bv.get_basic_blocks_at(
            emuRange[0])[0].incoming_edges[0].source
        white.append(preBB.start)
print("[x] try find missing arg at {}".format(preBB))
workCsel(uc, bv, lastCsel, Brinstruction, (preBB.start,
                                               emuRange[1]), textSecRange, white=white, depth=depth+1)
def workCsel(uc: Uc, bv: BinaryView, lastCsel: list, Brinstruction: list, emuRange: Tuple, textSecRange: Tuple, white: list = [], depth: int = 0):
try:
        Hook = uc.hook_add(UC_HOOK_CODE, avoidBlHook,
                           {"bv": bv, "white": white})
print(lastCsel)
print("[+] work at {} -- {}".format(hex(emuRange[0]), hex(emuRange[1])))
print("[+] cur search depth: {}".format(depth))
        regs = emuToGetRegInitState(uc, emuRange[0], lastCsel[1])
# 获取进入CSEL之前的寄存器状态
# 然后因为CSEL的赋值选择第一个还是第二个参数是和cond对应的，br跳转必然前面跟一个add类的计算指令来计算地址
# 也就是说，这里提供了两条指令的空间来让我们构造一对互补的b.cond ，于是就规避了可能误修改业务相关指令的麻烦

        destReg = lastCsel[0][2].text
        trueReg = lastCsel[0][5].text
        falseReg = lastCsel[0][8].text
        cond = lastCsel[0][11].text
        brTarget = Brinstruction[0][2].text
        curAddr = Brinstruction[1]
# 这里搜集一些指令的参数信息，具体为什么这么写因为bn的指令token就是这么约定的
# print(regs)
if debugMode:
print(destReg, trueReg, falseReg, cond, brTarget)

# hk = uc.hook_add(UC_HOOK_CODE, codeHook, {"bv": bv})

        recover_regisers(uc, regs)
if trueReg == "xzr" or trueReg == "wzr":  # 这个主要是处理uc不能读取arm的0寄存器的问题，我们要手动赋0
            uc.reg_write(ARM64_REG_MAP[destReg], 0)
else:
            uc.reg_write(ARM64_REG_MAP[destReg],
                         regs[trueReg])
# print(regs[trueReg])
        trueDest = emuToGetJumpReg(
            uc, lastCsel[1]+4, curAddr,  brTarget)

        recover_regisers(uc, regs)
if falseReg == "xzr" or falseReg == "wzr":
            uc.reg_write(ARM64_REG_MAP[destReg], 0)
else:
            uc.reg_write(ARM64_REG_MAP[destReg],
                         regs[falseReg])
# print(regs[falseReg])
        falseDest = emuToGetJumpReg(
            uc, lastCsel[1]+4, curAddr, brTarget)
if debugMode:
print("[+]  if ture then to:{} n else to:{}".format(
hex(trueDest), hex(falseDest)))
# print("[asm to replace]{}n[asm to replace]{}".format(bv.get_disassembly(
# curAddr-4), bv.get_disassembly(curAddr)))
        uc.hook_del(Hook)
if not (textSecRange[0] <= trueDest <= textSecRange[1]) or not (textSecRange[0] <= falseDest <= textSecRange[1]):  # 检查地址是否在text段范围内
print("[x] wrong dest occured,try to fix")
# 如果没有前驱基本块，说明此时处于函数的第一个基本块，要去找该函数的交叉引用
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
                ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
                preBB = bv.get_basic_blocks_at(ref[0].address)[
0]  # 获取交叉引用所处的基本块
                white.append(preBB.start)  # 把基本块开头加入跳转白名单
else:
                preBB = bv.get_basic_blocks_at(
                    emuRange[0])[0].incoming_edges[0].source  # 如果有前驱基本块，就获取它
                white.append(preBB.start)  # 把基本块开头加入跳转白名单
print("[x] try find missing arg at {}".format(preBB))
            workCsel(uc, bv, lastCsel, Brinstruction, (preBB.start,
                     emuRange[1]), textSecRange, white=white, depth=depth+1)
else:  # 如果正常就组装指令并patch
            buildOpAndPatch(bv, cond, trueDest, falseDest, curAddr)
except UcError as e: # 捕获到错误地址读写或其他错误行为
        uc.hook_del(Hook)
if e.errno == UC_ERR_READ_UNMAPPED or e.errno == UC_ERR_WRITE_UNMAPPED:
print("[x] unmapped R/W occured,try to fix    [{}    {}]".format(hex(
                uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
else:
print("[!!!] unhanddle error: {}   [{}    {}]".format(e, hex(
                uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
            ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
            preBB = bv.get_basic_blocks_at(ref[0].address)[0]
            white.append(preBB.start)
else:
            preBB = bv.get_basic_blocks_at(
                emuRange[0])[0].incoming_edges[0].source
            white.append(preBB.start)
print("[x] try find missing arg at {}".format(preBB))
        workCsel(uc, bv, lastCsel, Brinstruction, (preBB.start,
                                                   emuRange[1]), textSecRange, white=white, depth=depth+1)
def buildOpAndPatch(bv: binaryview, cond: str, trueDest: int, falseDest: int, curAddr: int):
    trueJmp = "b.{} #{}".format(cond, hex(trueDest-(curAddr-4)))
    falseJmp = "b.{} #{}".format(ARM64_CONDS[cond], hex(falseDest-curAddr))
print("[asm gen]{}  ->  {}".format(bv.get_disassembly(curAddr-4), trueJmp))
print("[asm gen]{}  ->  {}".format(bv.get_disassembly(curAddr), falseJmp))
    # 使用bn提供的指令转换api获得机械码
    bv.write(curAddr-4, Architecture['aarch64'].assemble(trueJmp))
    bv.write(curAddr, Architecture['aarch64'].assemble(falseJmp))
print("===================================================")
from binaryninja import *
from unicorn import *
from unicorn.arm64_const import *

CODE_BASE = 0x0
CODE_SIZE = 0x1200000+0x1000
STACK_BASE = 0x30000000
STACK_SIZE = 0x8000

ARM64_REG_MAP = {
'x0': UC_ARM64_REG_X0, 'x1': UC_ARM64_REG_X1, 'x2': UC_ARM64_REG_X2, 'x3': UC_ARM64_REG_X3,
'x4': UC_ARM64_REG_X4, 'x5': UC_ARM64_REG_X5, 'x6': UC_ARM64_REG_X6, 'x7': UC_ARM64_REG_X7,
'x8': UC_ARM64_REG_X8, 'x9': UC_ARM64_REG_X9, 'x10': UC_ARM64_REG_X10, 'x11': UC_ARM64_REG_X11,
'x12': UC_ARM64_REG_X12, 'x13': UC_ARM64_REG_X13, 'x14': UC_ARM64_REG_X14, 'x15': UC_ARM64_REG_X15,
'x16': UC_ARM64_REG_X16, 'x17': UC_ARM64_REG_X17, 'x18': UC_ARM64_REG_X18, 'x19': UC_ARM64_REG_X19,
'x20': UC_ARM64_REG_X20, 'x21': UC_ARM64_REG_X21, 'x22': UC_ARM64_REG_X22, 'x23': UC_ARM64_REG_X23,
'x24': UC_ARM64_REG_X24, 'x25': UC_ARM64_REG_X25, 'x26': UC_ARM64_REG_X26, 'x27': UC_ARM64_REG_X27,
'x28': UC_ARM64_REG_X28, 'x29': UC_ARM64_REG_X29,
'x30': UC_ARM64_REG_X30,
'sp': UC_ARM64_REG_SP,
'w0': UC_ARM64_REG_X0, 'w1': UC_ARM64_REG_X1, 'w2': UC_ARM64_REG_X2, 'w3': UC_ARM64_REG_X3,
'w4': UC_ARM64_REG_X4, 'w5': UC_ARM64_REG_X5, 'w6': UC_ARM64_REG_X6, 'w7': UC_ARM64_REG_X7,
'w8': UC_ARM64_REG_X8, 'w9': UC_ARM64_REG_X9, 'w10': UC_ARM64_REG_X10, 'w11': UC_ARM64_REG_X11,
'w12': UC_ARM64_REG_X12, 'w13': UC_ARM64_REG_X13, 'w14': UC_ARM64_REG_X14, 'w15': UC_ARM64_REG_X15,
'w16': UC_ARM64_REG_X16, 'w17': UC_ARM64_REG_X17, 'w18': UC_ARM64_REG_X18, 'w19': UC_ARM64_REG_X19,
'w20': UC_ARM64_REG_X20, 'w21': UC_ARM64_REG_X21, 'w22': UC_ARM64_REG_X22, 'w23': UC_ARM64_REG_X23,
'w24': UC_ARM64_REG_X24, 'w25': UC_ARM64_REG_X25, 'w26': UC_ARM64_REG_X26, 'w27': UC_ARM64_REG_X27,
'w28': UC_ARM64_REG_X28,
'wzr': None,
'xzr': None,
}
# 每个条件码逻辑上对应的互补的条件
ARM64_CONDS = {
'eq': 'ne',
'ne': 'eq',
'hs': 'lo',
'lo': 'hs',
'mi': 'pl',
'pl': 'mi',
'vs': 'vc',
'vc': 'vs',
'hi': 'ls',
'ls': 'hi',
'ge': 'lt',
'lt': 'ge',
'gt': 'le',
'le': 'gt',
'cs': 'cc',
'cc': 'cs',
}

def save_regisers(uc: Uc):
    regs = {}
for reg in ARM64_REG_MAP:
if ARM64_REG_MAP[reg] is not None:
            regs[reg] = uc.reg_read(ARM64_REG_MAP[reg])  # 读取所有寄存器信息并储存
return regs

def codeHook(uc: Uc, address, size, user_data):
    bv = user_data.get("bv")
    code = bv.get_disassembly(address)
    assert isinstance(bv, BinaryView)
if address >= 0x021e5c and address <= 0x21e74:
print("[{}]{}".format(
hex(address), code))
if address >= 0x000355f0 and address <= 0x00035668:
print("[{}]{}".format(
hex(address), code))

def recover_regisers(uc: Uc, regs: dict):
for reg in ARM64_REG_MAP:
if ARM64_REG_MAP[reg] is not None:
            uc.reg_write(ARM64_REG_MAP[reg], regs[reg])
# print("{}  =   {}".format(reg, hex(regs[reg])))

def emuToGetRegInitState(uc: Uc, start: int, end: int) -> dict:
    stack_top = STACK_BASE + STACK_SIZE - 0x100
    uc.reg_write(UC_ARM64_REG_SP, stack_top)  # 设置栈指针
# 根据arm调用约定，初始的栈顶必须写8个0x00
    uc.mem_write(stack_top, b"x00x00x00x00x00x00x00x00")
    uc.emu_start(start, end)  # 开启模拟
return save_regisers(uc)

def emuToGetJumpReg(uc: Uc, start: int, end: int, brTarget: str) -> int:
    uc.emu_start(start, end)
return uc.reg_read(ARM64_REG_MAP[brTarget])

debugMode = 1

def avoidBlHook(uc: Uc, address, size, user_data):
    bv = user_data.get("bv")
    white = user_data.get("white")  # 把传过来的白名单和bv取出来
    assert isinstance(bv, BinaryView)  # 不这样写编辑器不识别bv的类型
    code = bv.get_disassembly(address)  # 获取当前地址的指令
if "bl" in code:
for tar in white:
if hex(tar) in code:
if debugMode:
print("enter {}".format(hex(tar)))
break
else:  # 遍历白名单，如果遍历完都没有break，说明当前指令要被跳过
if debugMode:
print("[not {}] [skip {}] {}".format(
list(map(hex, white)), hex(address), code))
            uc.reg_write(UC_ARM64_REG_PC, address+4)  # 把pc设置为pc+4
if "b." in code:
for tar in white:
if hex(tar) in code:
if debugMode:
print("force jmp {}".format(hex(tar)))
# 这里如果遇到了白名单中的地址，直接把pc覆写成这个地址，即强制跳转
                uc.reg_write(UC_ARM64_REG_PC, tar)
break
else:
if debugMode:
print("skip unknown jmp target")
            uc.reg_write(UC_ARM64_REG_PC, address+4)  # 否则就跳过（不然也可能会被导到不知道哪里去）
# input()

def buildOpAndPatch(bv: binaryview, cond: str, trueDest: int, falseDest: int, curAddr: int):
    trueJmp = "b.{} #{}".format(cond, hex(trueDest-(curAddr-4)))
    falseJmp = "b.{} #{}".format(ARM64_CONDS[cond], hex(falseDest-curAddr))
print("[asm gen]{}  ->  {}".format(bv.get_disassembly(curAddr-4), trueJmp))
print("[asm gen]{}  ->  {}".format(bv.get_disassembly(curAddr), falseJmp))
    bv.write(curAddr-4, Architecture['aarch64'].assemble(trueJmp))
    bv.write(curAddr, Architecture['aarch64'].assemble(falseJmp))
print("===================================================")

def workCsel(uc: Uc, bv: BinaryView, lastCsel: list, Brinstruction: list, emuRange: Tuple, textSecRange: Tuple, white: list = [], depth: int = 0):
try:
        Hook = uc.hook_add(UC_HOOK_CODE, avoidBlHook,
                           {"bv": bv, "white": white})
print(lastCsel)
print("[+] work at {} -- {}".format(hex(emuRange[0]), hex(emuRange[1])))
print("[+] cur search depth: {}".format(depth))
        regs = emuToGetRegInitState(uc, emuRange[0], lastCsel[1])
# 获取进入CSEL之前的寄存器状态
# 然后因为CSEL的赋值选择第一个还是第二个参数是和cond对应的，br跳转必然前面跟一个add类的计算指令来计算地址
# 也就是说，这里提供了两条指令的空间来让我们构造一对互补的b.cond ，于是就规避了可能误修改业务相关指令的麻烦

        destReg = lastCsel[0][2].text
        trueReg = lastCsel[0][5].text
        falseReg = lastCsel[0][8].text
        cond = lastCsel[0][11].text
        brTarget = Brinstruction[0][2].text
        curAddr = Brinstruction[1]
# 这里搜集一些指令的参数信息，具体为什么这么写因为bn的指令token就是这么约定的
# print(regs)
if debugMode:
print(destReg, trueReg, falseReg, cond, brTarget)

# hk = uc.hook_add(UC_HOOK_CODE, codeHook, {"bv": bv})

recover_regisers(uc, regs)
if trueReg == "xzr" or trueReg == "wzr":  # 这个主要是处理uc不能读取arm的0寄存器的问题，我们要手动赋0
            uc.reg_write(ARM64_REG_MAP[destReg], 0)
else:
            uc.reg_write(ARM64_REG_MAP[destReg],
                         regs[trueReg])
# print(regs[trueReg])
        trueDest = emuToGetJumpReg(
            uc, lastCsel[1]+4, curAddr,  brTarget)

recover_regisers(uc, regs)
if falseReg == "xzr" or falseReg == "wzr":
            uc.reg_write(ARM64_REG_MAP[destReg], 0)
else:
            uc.reg_write(ARM64_REG_MAP[destReg],
                         regs[falseReg])
# print(regs[falseReg])
        falseDest = emuToGetJumpReg(
            uc, lastCsel[1]+4, curAddr, brTarget)
if debugMode:
print("[+]  if ture then to:{} n else to:{}".format(
hex(trueDest), hex(falseDest)))
# print("[asm to replace]{}n[asm to replace]{}".format(bv.get_disassembly(
# curAddr-4), bv.get_disassembly(curAddr)))
        uc.hook_del(Hook)
if not (textSecRange[0] <= trueDest <= textSecRange[1]) or not (textSecRange[0] <= falseDest <= textSecRange[1]):  # 检查地址是否在text段范围内
print("[x] wrong dest occured,try to fix")
# 如果没有前驱基本块，说明此时处于函数的第一个基本块，要去找该函数的交叉引用
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
                ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
                preBB = bv.get_basic_blocks_at(ref[0].address)[
0]  # 获取交叉引用所处的基本块
                white.append(preBB.start)  # 把基本块开头加入跳转白名单
else:
                preBB = bv.get_basic_blocks_at(
                    emuRange[0])[0].incoming_edges[0].source  # 如果有前驱基本块，就获取它
                white.append(preBB.start)  # 把基本块开头加入跳转白名单
print("[x] try find missing arg at {}".format(preBB))
workCsel(uc, bv, lastCsel, Brinstruction, (preBB.start,
                     emuRange[1]), textSecRange, white=white, depth=depth+1)
else:  # 如果正常就组装指令并patch
buildOpAndPatch(bv, cond, trueDest, falseDest, curAddr)
    
except UcError as e: # 捕获到错误地址读写或其他错误行为
        uc.hook_del(Hook)
if e.errno == UC_ERR_READ_UNMAPPED or e.errno == UC_ERR_WRITE_UNMAPPED:
print("[x] unmapped R/W occured,try to fix    [{}    {}]".format(hex(
                uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
else:
print("[!!!] unhanddle error: {}   [{}    {}]".format(e, hex(
                uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
            ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
            preBB = bv.get_basic_blocks_at(ref[0].address)[0]
            white.append(preBB.start)
else:
            preBB = bv.get_basic_blocks_at(
                emuRange[0])[0].incoming_edges[0].source
            white.append(preBB.start)
print("[x] try find missing arg at {}".format(preBB))
workCsel(uc, bv, lastCsel, Brinstruction, (preBB.start,
                                                   emuRange[1]), textSecRange, white=white, depth=depth+1)

def workCset(uc: Uc, bv: BinaryView, lastCset: list, Brinstruction: list, emuRange: Tuple, textSecRange: Tuple, white: list = [], depth: int = 0):
try:
        Hook = uc.hook_add(UC_HOOK_CODE, avoidBlHook,
                           {"bv": bv, "white": white, "end": emuRange[1]})
print(lastCset)
print("[+] work at {} -- {}".format(hex(emuRange[0]), hex(emuRange[1])))
print("[+] cur search depth: {}".format(depth))
        regs = emuToGetRegInitState(uc, emuRange[0], lastCset[1])

        destReg = lastCset[0][2].text
        cond = lastCset[0][5].text
        brTarget = Brinstruction[0][2].text
        curAddr = Brinstruction[1]
if debugMode:
print(destReg, cond, brTarget)
recover_regisers(uc, regs)
        uc.reg_write(ARM64_REG_MAP[destReg], 1)
        trueDest = emuToGetJumpReg(
            uc, lastCset[1]+4, curAddr,  brTarget)
recover_regisers(uc, regs)
        uc.reg_write(ARM64_REG_MAP[destReg], 0)
        falseDest = emuToGetJumpReg(
            uc, lastCset[1]+4, curAddr, brTarget)
if debugMode:
print("[+]  if ture then to:{} n else to:{}".format(
hex(trueDest), hex(falseDest)))
# print("[asm to replace]{}n[asm to replace]{}".format(bv.get_disassembly(
#     curAddr-4), bv.get_disassembly(curAddr)))
        uc.hook_del(Hook)
if not (textSecRange[0] <= trueDest <= textSecRange[1]) or not (textSecRange[0] <= falseDest <= textSecRange[1]):
print("[x] wrong dest occured,try to fix")
print("incoming edges: {}".format(
                bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges))
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
                ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
                preBB = bv.get_basic_blocks_at(ref[0].address)[0]
                white.append(preBB.start)
else:
                preBB = bv.get_basic_blocks_at(
                    emuRange[0])[0].incoming_edges[0].source
                white.append(preBB.start)
print("[x] try find missing arg at {}".format(preBB))
workCset(uc, bv, lastCset, Brinstruction, (preBB.start,
                     emuRange[1]), textSecRange, white=white, depth=depth+1)
else:
buildOpAndPatch(bv, cond, trueDest, falseDest, curAddr)

    
except UcError as e:
        uc.hook_del(Hook)
if e.errno == UC_ERR_READ_UNMAPPED or e.errno == UC_ERR_WRITE_UNMAPPED:
print("[x] unmapped R/W occured,try to fix    [{}    {}]".format(hex(
                uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
else:
print("[!!!] unhanddle error: {}   [{}    {}]".format(e, hex(
                uc.reg_read(UC_ARM64_REG_PC)), bv.get_disassembly(uc.reg_read(UC_ARM64_REG_PC))))
if len(bv.get_basic_blocks_at(emuRange[0])[0].incoming_edges) == 0:
            ref = list(bv.get_code_refs(emuRange[0]))
print("{}  ref {}".format(hex(emuRange[0]), ref))
            preBB = bv.get_basic_blocks_at(ref[0].address)[0]
            white.append(preBB.start)
else:
            preBB = bv.get_basic_blocks_at(
                emuRange[0])[0].incoming_edges[0].source
            white.append(preBB.start)
print("[x] try find missing arg at {}".format(preBB))
workCset(uc, bv, lastCset, Brinstruction, (preBB.start,
                                                   emuRange[1]), textSecRange, white=white, depth=depth+1)

def solve(bv: BinaryView):
    uc = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
    uc.mem_map(CODE_BASE, CODE_SIZE, UC_PROT_ALL)  # 分配text段内存
    uc.mem_map(STACK_BASE, STACK_SIZE, UC_PROT_ALL)  # 分配栈内存
for segment in bv.segments:   # 用bn API遍历所有段
if segment.readable:
            start = segment.start
            end = segment.end
            size = end-start
print("[+] Mapping segment: [{}]".format(hex(segment.data_length)))
            content = bv.read(start, size)  # 读取段数据
            uc.mem_write(start, content)  # 写入uc模拟器
    lastCsel = None
    lastCset = None
    nextWork = None   # 记录最后遇到的是csel还是cset
for instruction in bv.instructions:  # 遍历所有指令
        curAddr = instruction[1]
# print(curAddr)
if instruction[0][0].text == "csel":
            lastCsel = instruction
            nextWork = "csel"
if instruction[0][0].text == "cset":
            lastCset = instruction
            nextWork = "cset"
if instruction[0][0].text == "br":
            tags = bv.get_functions_containing(curAddr)[0].tags  # 获取当前函数的所有tag
            curTag = None
for tag in tags:
if tag[1] == curAddr:  # 寻找br指令上的tag
                    curTag = tag[2]
break
# 查看是否为间接控制流
if curTag is None or not (curTag.type.name == "Unresolved Indirect Control Flow"):
continue
# print(hex(curAddr))
            curBB = bv.get_basic_blocks_at(curAddr)[0]   # 获取当前指令所在的基本块
            curFunc = bv.get_functions_containing(curAddr)[0]  # 获取当前指令所在的函数
# print(curBB)
if nextWork is None:
continue
try:
if nextWork == "csel":
if lastCsel[1] < curFunc.start or lastCsel[1] > curBB.end:  # 判断csel指令是否在当前函数内
continue
workCsel(uc, bv, lastCsel, instruction,
                             (curBB.start, curBB.end), (0xf4c0, 0x591d0), white=[curBB.start])
                    nextWork = None
                elif nextWork == "cset":
if lastCset[1] < curFunc.start or lastCset[1] > curBB.end:  # 判断cset指令是否在当前函数内
continue
workCset(uc, bv, lastCset, instruction,
                             (curBB.start, curBB.end), (0xf4c0, 0x591d0), white=[curBB.start])
                    nextWork = None
            
except Exception as e:  # 捕获预期外的异常
print("[{}] Error: {}".format(
hex(uc.reg_read(UC_ARM64_REG_PC)), e))

solve(bv)
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]