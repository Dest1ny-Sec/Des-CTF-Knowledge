---
title: 从data段中加载PE Executable——2022蓝帽杯Reverse Loader Writeup
contest: 蓝帽杯 2022 Reverse
year: 2022
difficulty: hard
vuln_type: reverse
tags: [PE加载器, 无文件PE, IAT修复, Base Relocation, CRC32, GetProcAddress, PEB, LDR, InMemoryOrderModuleList, Pell方程, big num, nim]
attack_chain:
  - VirtualProtect 把 .data 段设为 RWX 加载内嵌 PE dump
  - 修改栈顶 rip 跳转到 code+0x34000 主逻辑
  - gs:[0x60] 拿 PEB 指针 → PEB:[0x18] 拿 LDR 指针
  - LDR:[0x20] 拿 InMemoryOrderModuleList 遍历已加载模块
  - 解析 kernel32.dll 的 IMAGE_NT_HEADERS + IMAGE_DATA_DIRECTORY 拿 Export table
  - 用 0xEDB88320 多项式 CRC32 校验函数名查 GetProcAddress
  - lodsd 取下一个 checksum 循环查 LoadLibraryA
  - 处理 Import Table IMAGE_IMPORT_DESCRIPTOR FirstThunk 填绝对地址
  - 处理 Base Relocation Table 遍历每个要改写地址加上 code 基址
  - 跳转 OEP 后是 nim 编译逻辑：input 解析 big num
  - 约束 num1*num1-11*num2*num2 == 9 + big1 < num1 < big2
  - sage 算 Pell 方程 x²-11y²=1 连分数收敛子
  - 复合 (x1,y1)×(x2,y2) 找 num1 = 3x, num2 = 3y
key_payload: 'flag{%018d%018d}' % (num1, num2)
one_liner: 手写 PE Loader 从 .data 段加载无文件 PE，IAT 用 CRC32 查表 + Base Relocation；nim 关键逻辑是 Pell 方程 x²-11y²=1 求解。
lesson: 无文件 PE 加载 = VirtualProtect RWX + 手写 IAT (CRC 查函数名) + Base Relocation; Pell 方程 x²-Dy²=1 用连分数 convergents + 复合群无限解。
quality: high
---

# 从data段中加载PE Executable——2022蓝帽杯Reverse Loader Writeup

## 概览
- **来源**: ctfiot 48420
- **赛事**: 蓝帽杯 2022 Reverse
- **题目**: Loader - 从 .data 段加载 PE 执行
- **难度**: ⭐⭐⭐⭐

## Loader 部分 (PE 加载器)
1. **VirtualProtect** 把 .data 段设为 RWX
2. **改栈顶 rip** 跳到 code+0x34000
3. **PEB 链**:
   - `gs:[0x60]` → PEB
   - `PEB:[0x18]` → LDR (PEB_LDR_DATA)
   - `LDR:[0x20]` → InMemoryOrderModuleList 双向链表
4. **Export table 解析** (kernel32.dll):
   - `IMAGE_NT_HEADERS.OptionalHeader.DataDirectory[0]` = Export table offset
   - `AddressOfNames` (rbx+0x20) 遍历函数名
5. **CRC32 查函数名**:
   - 多项式 `0xEDB88320`
   - 命中 GetProcAddress → AddressOfFunctions 查 index
   - 命中 LoadLibraryA
6. **IAT 修复**:
   - 遍历 IMAGE_IMPORT_DESCRIPTOR.FirstThunk
   - LoadLibraryA + GetProcAddress 填绝对地址
7. **Base Relocation**:
   - 遍历每个要改写地址：`addr = &code + offset`
8. **跳 OEP** 进入 nim 主逻辑

## 关键逻辑 (Nim 大数)
```nim
let big1 = 0x100000000000000
let big2 = 0x1000000000000000
let num1 = parseBigNum(input1)
let num2 = parseBigNum(input2)
assert big1 < num1 and num1 < big2
assert num1*num1 - 11*num2*num2 == 9
```

## Pell 方程求解
```python
# sage
cf = continued_fraction(sqrt(11))
cs = cf.convergents()
for each in cs:
    x1, y1 = each.numer(), each.denom()
    if x1^2 - 11*y1^2 == 1: break
for each in cs[1:]:
    x2, y2 = each.numer(), each.denom()
    if x2^2 - 11*y2^2 == 1: break
D = 11
big1 = 0x100000000000000
big2 = 0x1000000000000000
while True:
    x = x1*x2 + D*y1*y2
    y = x1*y2 + x2*y1
    if big1 < x*3 < big2: break
    x2, y2 = x1, y1
    x1, y1 = x, y
num1, num2 = x*3, y*3
print('flag{%018d%018d}' % (num1, num2))
```

## 输出格式
- `flag{000xxx...000xxx}` 18 位 num1 + 18 位 num2
