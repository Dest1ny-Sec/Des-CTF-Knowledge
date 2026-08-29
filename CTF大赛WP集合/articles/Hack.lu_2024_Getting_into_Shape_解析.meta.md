---
title: Hack.lu 2024 Getting into Shape 解析
contest: Hack.lu 2024
year: 2024
difficulty: hard
vuln_type: reverse
tags: [rev, wasm, ttf, rust, regex-automata, cipher, expand-32-byte-k, salsa20]
attack_chain:
  - TTF文件包含WASM二进制
  - 提取 0x1eb9c 偏移 0x12841b 长度
  - d_Usersmsanftcargoregistrysrci 路径
  - Rust regex-automata 0.4.8 + cipher 0.4.4
  - StreamCipherError
  - 关键字 expand 32-byte k (Salsa20 constant)
  - flag{([^{}]*)} 正则
  - "yasss!!" emoji 0xf09f988c 0xf09f9285
  - "nahf09f9890f09f9890" 隐藏flag
key_payload: expand 32-byte k (Salsa20 constant)
one_liner: Hack.lu 2024 Getting into Shape：TTF嵌WASM+Rust cipher+Salsa20
lesson: Rust WASM二进制可藏在字体文件TTF中
quality: high
---

# Hack.lu 2024 Getting into Shape 解析

## 题目信息
- 比赛：Hack.lu 2024
- 题目：Getting into Shape
- 类别：Reverse（WASM + Rust）

## 关键攻击链
### 1. WASM 提取
```python
with open('challenge.ttf', 'rb') as file:
    read_bytes = file.read()

with open('challenge.wasm', 'wb') as ff:
    start = 0x1eb9c
    end = start + 0x12841b
    ff.write(read_bytes[start:end])
```

### 2. 关键路径
- `/Users/msanft/.cargo/registry/src/index.crates.io-6f17d22bba15001f/`
- `regex-automata-0.4.8/src/util/pool.rs`
- `cipher-0.4.4/src/stream.rs`
- Rust 项目：regex-automata 0.4.8 + cipher 0.4.4

### 3. 关键发现
- `StreamCipherError`
- 关键字 `expand 32-byte k`（Salsa20 魔数常量）
- 正则 `flag{([^{}]*)}`
- 错误信息："Couldn't copy buffer contents"
- 路径：`/Users/msanft/Documents/Documents - Moritz's MacBo...`

### 4. 隐藏内容
- `nahf09f9890f09f9890yasss!!f09f988cf09f9285`
- 含义：nah + 😠😠 + yasss!! + 😌🤅
- flag 隐藏在 emoji 编码间

## 评分
- quality: high（TTF 藏 WASM + Rust cipher + Salsa20 魔数识别）
