---
title: 国赛babytree 赛题解析
contest: 国赛 babytree (Swift)
year: 2024
difficulty: medium
vuln_type: reverse
tags: [Swift逆向, swiftc -dump-ast, var b/k/r0/r1/r2/r3, key循环移位, 反向异或, 42字节目标, [UInt8]]
attack_chain:
  - Swift babytree 逆向 (swiftc -dump-ast hello.swift)
  - var key = "345y" (4 字节)
  - var data = CommandLine.arguments[1]
  - check(data, key) 函数
  - var b = [UInt8](data.utf8)
  - var k = [UInt8]("345y".utf8) = [51, 52, 53, 121]
  - for i in 0..b.count-4:
  -   r0,r1,r2,r3 = b[i..i+3]
  -   b[i+0] = r2 ^ ((k[0] + (r0>>4)) & 0xff)
  -   b[i+1] = r3 ^ ((k[1] + (r1>>2)) & 0xff)
  -   b[i+2] = r0 ^ k[2]
  -   b[i+3] = r1 ^ k[3]
  -   k = [k[1], k[2], k[3], k[0]]  # 循环左移
  - return b == [88,35,88,225,7,201,57,94,77,56,75,168,72,218,64,91,16,101,32,207,73,130,74,128,76,201,16,248,41,205,103,84,91,99,79,202,22,131,63,255,20,16]
  - 反向: 倒序循环 + k 循环右移 + r0/r1/r2/r3 恢复
key_payload: '[88,35,88,225,...] + key 循环移位反推'
one_liner: Swift babytree 逆向：key="345y" 4 字节循环移位 + r0/r1/r2/r3 异或 + 42 字节目标反推。
lesson: Swift 编译产物可用 swiftc -dump-ast 看 AST 还原源码; 4 字节 key 循环移位加密是经典 pattern; 反向算法倒序循环 + k 循环右移。
quality: medium
---

# 国赛babytree 赛题解析

## 概览
- **来源**: ctfiot 162996 (看雪 wenling)
- **类型**: Swift 字节码逆向
- **难度**: ⭐⭐⭐

## 还原源码
```swift
func check(encoded: String, keyValue: String) -> Bool {
    var b = [UInt8](encoded.utf8)
    var k = [UInt8](keyValue.utf8)
    var r0, r1, r2, r3: UInt8
    for i in 0...b.count-4 {
        r0 = b[i]; r1 = b[i+1]; r2 = b[i+2]; r3 = b[i+3]
        b[i+0] = r2 ^ ((k[0] + (r0 >> 4)) & 0xff)
        b[i+1] = r3 ^ ((k[1] + (r1 >> 2)) & 0xff)
        b[i+2] = r0 ^ k[2]
        b[i+3] = r1 ^ k[3]
        let temp = k[0]
        k[0] = k[1]; k[1] = k[2]; k[2] = k[3]; k[3] = temp
    }
    return b == [88, 35, 88, 225, 7, 201, 57, 94, 77, 56, 75, 168, 72, 218, 64, 91, 16, 101, 32, 207, 73, 130, 74, 128, 76, 201, 16, 248, 41, 205, 103, 84, 91, 99, 79, 202, 22, 131, 63, 255, 20, 16]
}
```

## 反向解密
```python
b = [88, 35, 88, 225, 7, 201, 57, 94, 77, 56, 75, 168, 72, 218, 64, 91, 16, 101, 32, 207, 73, 130, 74, 128, 76, 201, 16, 248, 41, 205, 103, 84, 91, 99, 79, 202, 22, 131, 63, 255, 20, 16]
k = [121, 51, 52, 53]  # "345y" 字节 (注意顺序: 'y' '3' '4' '5' = [121,51,52,53])
for i in range(len(b) - 4, -1, -1):
    # k 循环右移
    k[1], k[2], k[3], k[0] = k[0], k[1], k[2], k[3]
    r1 = k[3] ^ b[i+3]
    r0 = k[2] ^ b[i+2]
    r3 = ((k[1] + (r1 >> 2)) & 0xff) ^ b[i+1]
    r2 = ((k[0] + (r0 >> 4)) & 0xff) ^ b[i]
    b[i], b[i+1], b[i+2], b[i+3] = r0, r1, r2, r3
print(''.join(chr(c) for c in b))
```

## 工具
- `swiftc -dump-ast hello.swift` 看 AST
- Xcode Symbols 还原类型

## 教学
- Swift 编译产物逆向: swiftc -dump-ast + IDA + Hopper
- 4 字节 key 循环移位加密: 反向时倒序 + 循环右移
- `>>` (右移) + `& 0xff` 掩码是密码学常用
