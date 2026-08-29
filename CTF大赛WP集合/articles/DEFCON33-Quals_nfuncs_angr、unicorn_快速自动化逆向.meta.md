---
title: DEFCON33-Quals nfuncs angr、unicorn 快速自动化逆向
contest: DEFCON
year: 2025
difficulty: hard
vuln_type: reverse
tags: [angr-symbolic, unicorn-emulation, smc, virtualprotect, capstone, pefile, hook-loop, lut, memcmp]
attack_chain:
  - angr 项目用 read hook 收集 symbolic byte
  - capstone 提取 8 个 cmp/test 值
  - 约束求解 (input[i] == target - 13)
  - unicorn 模拟执行获取 VirtualProtect smc 内容
  - 把 smc 写回 PE 文件
  - checkpoint 记录下次 FUN_VA
  - 反复 hook 循环直到 memcmp 命中
  - 提取最终 ans
key_payload: angr + unicorn 混合符号执行 + SMC 自修改
one_liner: DEFCON 33 Quals nfuncs 逆向题，angr + unicorn 联合自动化求解 8 字节表查找链。
lesson: 现代 DEFCON 逆向题常用 SMC 自修改代码 + 多层函数调用，需要 angr 符号执行 + unicorn 模拟混合。
quality: high
---

DEFCON 33 Quals `nfuncs` 快速自动化逆向，作者 SleepAlone（看雪论坛）。

**核心思路**
逆向题有大量 SMC（self-modifying code），需要用 angr 符号执行找 input + 用 unicorn 模拟执行取 smc 内容，两者交替循环。

**第一阶段：angr 符号执行**
```python
class ReadHook(angr.SimProcedure):
    def run(self, fd, buf, cnt):
        sym = claripy.BVS(f"input_{len(input_bytes)}", 8)
        input_bytes.append(sym)
        self.state.memory.store(buf, sym)
        # 检查 LUT (look-up table) 标记
        value = self.state.solver.eval(self.state.memory.load(buf-0x108, 1), cast_to=int)
        if value == 13 + len(input_bytes) - 1:
            is_lut = True
        # 收 8 个 cmp/test 值
        if len(input_bytes) == 8 and is_lut:
            cmps = collect_cmp_value(FUN_VA)
            for i, target in enumerate(cmps):
                self.state.solver.add(input_bytes[i] == target - 13)
```

**第二阶段：unicorn 模拟 + SMC 写回**
```python
mu = Uc(UC_ARCH_X86, UC_MODE_64)
mu.mem_map(STACK_ADDR, STACK_SIZE)
# hook VirtualProtect 抓 smc 数据
def hook_instruction(uc, address, size, user_data):
    if address == 0xDEADBEEF100:  # VirtualProtect stub
        addr = uc.reg_read(UC_X86_REG_RCX)
        size = uc.reg_read(UC_X86_REG_RDX)
        smcs[addr] = uc.mem_read(addr, size)
        # 模拟 ret
        uc.reg_write(UC_X86_REG_RIP, ...)
        uc.reg_write(UC_X86_REG_RSP, uc.reg_read(UC_X86_REG_RSP) + 8)
    elif address == 0x1A703AA78:  # read stub
        if ans:
            byte = ans.pop()
            uc.mem_write(uc.reg_read(UC_X86_REG_RDX), bytes([byte]))
            # 模拟 ret
```

**第三阶段：循环迭代**
```python
while True:
    ANS = find_ans(FUN_VA, file_path=PE_PATH)  # angr 符号执行
    ans = bytearray(reversed(ANS))
    smcs = {}
    mu.emu_start(FUN_VA, FUN_VA + CODE_EXEC_LIMIT)  # unicorn 模拟
    
    # smc 写回 PE 文件
    for addr, data in smcs.items():
        for section in pe.sections:
            if sectionName == b'.text':
                f.seek(section.PointerToRawData + addr - start)
                f.write(data)
                break
    FUN_VA = addr  # checkpoint
    store_ans(ANS)
    store_checkpoint(addr)
```

**关键细节**
- `find_avoid_address` 用 capstone 找 find/avoid 的 mov 地址
- `collect_cmp_value` 用 capstone detail mode 提取前 8 个 cmp/test 操作数
- LUT 标记判断：8 字节输入地址前 0x108 偏移是 `13 + len(input_bytes) - 1` 时为表查找
- memcmp hook：触发时调用 `decrypt(key, enc_text)` 反查密钥 + 写回 ans_address-7

整题出题思路：用多层函数包装 + SMC 让静态分析工具失效，必须自动化 hook + 模拟才能跑通。
