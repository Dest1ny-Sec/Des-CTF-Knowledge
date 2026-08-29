---
title: Unicorn-BinaryNinja 去除 csel-br 间接跳转混淆
contest: 技术文章 (CSDN 转载)
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [unicorn_engine, binaryninja, arm64_obfuscation, csel_cset, indirect_branch, smc_emulation, code_patch, b_cond_pair, reverse_advanced]
attack_chain: BN 遍历所有指令找 csel/cset+br 间接跳转对 → Unicorn 模拟执行两次 (trueReg/falseReg 各一次) 收集寄存器 → 计算 trueDest/falseDest → 验证是否在 text 段范围内 → 构造 b.cond 互补指令对 (b.eq/b.ne) → bv.write 覆盖原指令
key_payload: Architecture['aarch64'].assemble("b.eq #0x123") / uc.emu_start(lastCsel[1]+4, curAddr) / ARM64_CONDS = {'eq':'ne','ne':'eq',...}
one_liner: 基于 Unicorn + BinaryNinja 的 ARM64 csel-br 间接跳转混淆自动化去除插件源码，逆向工程高级混淆的标配工具链。
lesson: 间接跳转混淆去除的核心是"分别模拟条件 true/false 两条路径"收集寄存器，确定 br Xn 的目标后用 b.cond 互补对替换。
quality: high
---
