---
title: 2024 KCTF 大赛 - 第十题《试探》设计思路及解析
contest: KCTF大赛
year: 2024
difficulty: medium
vuln_type: [reverse, misc_math]
tags: [拼图游戏, 0元素移动轨迹注册码, shellcode花指令, NtAddBootEntry, TpAllocWait, TpSetWait, 字符串加密隐藏, 0x2A替换, FD/FF/FE EB无效指令去混淆]
attack_chain: IDA 看 main 调 NtAddBootEntry + TpAllocWait + TpSetWait → 怀疑 shellcode 注入 → 找到 6050 处的 shellcode 复制到 75C0 → 创建 2 线程跑 shellcode + 等待答案 → shellcode 有大量花指令（FD EB 1F 3E 1C EB EB 等 6 字节无效）→ 写 1.py 替换无效指令为 NOP → 写 2.py 还原 0x2A → 0x00 → 看到 3x3 拼图算法 → 0 在初始 {0,1,3; 5,2,6; 4,7,8} → 目标 {1,2,3; 4,5,6; 7,8,0} → 0 元素每次移动的索引就是注册码
key_payload: 011110202122 ; 3 字节无效指令 FD EB 1F 3E 1C EB EB / FF EB 15 3E 1D EB FB / FE EB 18 3E 1C EB EB ; 初始棋盘 {0,1,3;5,2,6;4,7,8} ; 目标 {1,2,3;4,5,6;7,8,0}
one_liner: shellcode 拼图游戏 + 0 元素轨迹做注册码 + 6 字节花指令去混淆。
lesson: 无效指令 NOP 替换 + 0x2A 字节还原是 shellcode 混淆常见两步。
quality: high
---
# 2024 KCTF 大赛 - 第十题《试探》设计思路及解析

**出题战队 天外星系 · 一血 hzqmwne 用时 1h48m18s · 10 队提交**

## 题目分析

丢 IDA 看 main：
```c
// kctf + input + 0x6050 处的 shellcode → 复制到 0x75C0
// 创建 2 线程：
//   线程 A：执行 0x75C0 的 shellcode
//   线程 B：等待答案并输出 "ok!" 或 "no!"
```

主函数调 `ntdll!NtAddBootEntry` / `TpAllocWait` / `TpSetWait` → 怀疑 shellcode 注入。

## 去混淆

shellcode 在 `0x140006050`，不能直接 F5（混淆）。**无效指令特征码**只有 3 种 6 字节序列：

```
FD EB 1F 3E 1C EB EB
FF EB 15 3E 1D EB FB
FE EB 18 3E 1C EB EB
```

**1.py** 替换无效指令为 NOP：

```python
def replace_bytes_and_preceding(file_path, search_bytes, replace_byte, preceding_length):
    data = open(file_path, 'rb').read()
    modified = bytearray(data)
    start = 0
    while start < len(modified):
        index = modified.find(bytes.fromhex(search_bytes), start)
        if index == -1: break
        replace_start = max(0, index - preceding_length)
        modified[replace_start:index + len(bytes.fromhex(search_bytes))] = bytes.fromhex(replace_byte) * (len(bytes.fromhex(search_bytes)) + preceding_length)
        start = index + len(bytes.fromhex(search_bytes))
    open(file_path, 'wb').write(modified)

preceding_length = 11
replace_bytes_and_preceding('test3.exe', 'FD EB 1F 3E 1C EB EB', '90', preceding_length)
replace_bytes_and_preceding('test3.exe', 'FF EB 15 3E 1D EB FB', '90', preceding_length)
replace_bytes_and_preceding('test3.exe', 'FE EB 18 3E 1C EB EB', '90', preceding_length)
```

**2.py** 还原 `0x2A → 0x00`（被混淆时 0 写成 0x2A）：

```python
def replace_specific_byte_in_range(file_path, search_bytes, search_byte, replace_byte, offset_start, offset_end):
    data = open(file_path, 'rb').read()
    modified = bytearray(data)
    start = 0
    while start < len(modified):
        index = modified.find(bytes.fromhex(search_bytes), start)
        if index == -1: break
        for i in range(index + offset_start, min(index + offset_end, len(modified))):
            if modified[i] == int.from_bytes(bytes.fromhex(search_byte), 'little'):
                modified[i] = int.from_bytes(bytes.fromhex(replace_byte), 'little')
        start = index + len(bytes.fromhex(search_bytes))
    open(file_path, 'wb').write(modified)

replace_specific_byte_in_range('test3.exe', '57 50 51 56 E8 FF FF FF FF C0', '2A', '00', 0x2C, 0xEA7 + 0x2C)
```

## 拼图求解

**初始棋盘**
```
0 1 3
5 2 6
4 7 8
```

**目标棋盘**
```
1 2 3
4 5 6
7 8 0
```

3x3 拼图只有 9!/2 = 181440 状态，BFS 即可。每次移动 0 后**0 的索引**就是注册码的一位：

| 步骤 | 移动 | 0 的索引 | 棋盘 |
|------|------|----------|------|
| 1 | 右 | 1 | 1 0 3 / 5 2 6 / 4 7 8 |
| 2 | 下 | 4 | 1 2 3 / 5 0 6 / 4 7 8 |
| 3 | 左 | 3 | 1 2 3 / 0 5 6 / 4 7 8 |
| 4 | 下 | 6 | 1 2 3 / 4 5 6 / 0 7 8 |
| 5 | 右 | 7 | 1 2 3 / 4 5 6 / 7 0 8 |
| 6 | 右 | 8 | 1 2 3 / 4 5 6 / 7 8 0 |

注册码 = `011110202122`（初始 0 索引 0 + 6 步轨迹）
