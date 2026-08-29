---
title: DamCTF and Midnight Sun CTF Qualifiers pwn部分wp
contest: DamCTF 2023 / Midnight Sun CTF 2023
year: 2023
difficulty: medium
vuln_type: fmt_string
tags: [pwn, golden-banana, text-adventure, gets, fmt-string, bing-ai, 房间指针劫持]
attack_chain:
  - Golden Banana: 文字冒险游戏+Bing AI生成的剧情
  - main中game结构体存房间信息
  - 输入选项处gets栈溢出
  - printf(l->description) 格式化字符串泄露栈地址
  - 第二次gets溢出覆盖选项结构体跳到SECRET ROOM
  - SECRET ROOM直接输出flag
key_payload: gets(g.input_buf); printf(l->description)  # fmt-string leak
one_liner: DamCTF 2023 Golden Banana：gets栈溢出+fmt-string劫持房间指针
lesson: gets+printf描述信息可fmt-string泄露地址
quality: high
---

# DamCTF and Midnight Sun CTF Qualifiers pwn部分wp

## 题目信息
- 比赛：DamCTF 2023 Quals / Midnight Sun CTF 2023
- 作者：X1ng（看雪论坛）
- 涵盖：pwn 部分

## 关键攻击链
### DamCTF 2023 - The Quest for the Golden Banana
- 文字冒险游戏，剧情由 Bing AI 生成
- main 函数 `game` 结构体存所有房间信息
- 每个选项结构体保存选择后到达的房间地址
- **房间文件里有 SECRET ROOM** 直接输出 flag
- 输入选项处 `gets(g.input_buf)` 栈溢出
- 输出描述 `printf(l->description)` 格式化字符串
- 输出选项 `printf("%d: %s", i+1, l->choices[i].description)`

### 利用步骤
1. `gets` 溢出覆盖房间描述 → 触发 fmt-string
2. 泄露栈地址
3. 第二次 `gets` 溢出覆盖选项结构体中目标房间指针
4. 跳转到 SECRET ROOM 输出 flag

```python
from pwn import *
import sys, time
context.log_level = 'debug'
context.arch = 'amd64'

def exp(ip, port):
    libc = ELF("./libc.so.6")
    # 第一轮 fmt-string leak
    # 第二轮劫持选项结构体指针
```

### 关键坑
- `gets` 是 x0a (`\n`) 截断而非 `\x00` 截断
- 卡了作者很久

## 评分
- quality: high（完整 exp 思路 + 关键坑点提示）
