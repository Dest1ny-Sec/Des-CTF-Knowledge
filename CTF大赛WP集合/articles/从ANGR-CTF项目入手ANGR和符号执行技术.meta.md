---
title: 从ANGR-CTF项目入手ANGR和符号执行技术
contest: jakespringer/angr_ctf 训练营
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [angr, 符号执行, SimProcedure, hook, veritesting, reverse]
attack_chain:
  - 加载 angr Project 设定 base_addr 与 auto_load_libs=False
  - factory.entry_state 创建符号化初始状态
  - claripy.BVS 创建符号向量绑定寄存器/内存
  - simgr.explore(find=目标, avoid=陷阱) 反向求解
  - @project.hook 替换目标函数直接返回 eax
  - SimProcedure 类替换库函数（check_equals/scanf）避开路径爆炸
  - project.hook_symbol 按函数名挂 SimProcedure
  - 启用 veritesting=True 自动合并路径
  - 处理静态编译 strlen/共享库 validate 入口函数
  - 任意读通过 %7$s 格式化字符串符号化
key_payload: 'simgr.explore(find=target, avoid=un_target) + BVS(password, 8*16) + solver.eval()'
one_liner: angr-CTF 15 关系统训练，从 find/avoid 路径搜索到 SimProcedure 替换库函数避爆。
lesson: SimProcedure 替代 check_equals + veritesting 是处理 2^16 路径爆炸的标准姿势；hook_symbol 比 hook(addr) 健壮，符号化 stdin 写入 SimFile 即可虚拟文件读取。
quality: high
---

# 从ANGR-CTF项目入手ANGR和符号执行技术

## 概览
- **来源**: ctfiot.com 285534，jakespringer/angr_ctf 训练项目
- **目标**: 掌握 angr 符号执行框架 15 关全部解法
- **难度**: ⭐⭐ (入门到中级)

## 15 关核心 API
1. `00_angr_find` - find=目标地址 explore
2. `01_angr_avoid` - 同时给 avoid 避陷阱地址
3. `02_angr_find_condition` - 用 stdout 输出 'Good Job.'/'Try again.' 当 find/avoid
4. `03_angr_symbolic_registers` - BVS 绑 eax/ebx/edx
5. `04_angr_symbolic_stack` - blank_state + stack_push
6. `05_angr_symbolic_memory` - memory.store(addr, BVS, endness=LE)
7. `06_angr_symbolic_dynamic_memory` - 篡改 buffer 指针到 BSS 伪造堆块
8. `07_angr_symbolic_file` - SimFile + fs.insert + 劫持文件名全局指针
9. `08_angr_constraints` - 读取目标 buffer 做变换后 add_constraints
10. `09_angr_hooks` - @project.hook(addr) 直接改 eax
11. `10_angr_simprocedures` - SimProcedure 类 + hook_symbol 替换复杂函数
12. `11_angr_sim_scanf` - SimProcedure 替换 __isoc99_scanf 返回 2 个 BVS
13. `12_angr_veritesting` - simgr(veritesting=True) 自动合并动态分支
14. `13_angr_static_binary` - hook 静态 strlen 入口 0x4013b0
15. `14_angr_shared_library` - 直接在 .so validate 入口 0x1234 起状态
16. `15_angr_arbitrary_read` - 符号化 "%7$s" 触发格式化字符串读

## 核心技巧
- `auto_load_libs=False` 显著提速
- `add_options={angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS}` 防路径警告
- `endness=proj.arch.memory_endness` 必须指定否则报警
- `cast_to=bytes` 转 bytes，`posix.dumps(0)` 拿 stdin

## flag / 验证
- 训练题，flag 形如 "MSWKNJNAVTTOZMRY"
