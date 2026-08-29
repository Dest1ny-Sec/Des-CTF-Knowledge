---
title: DataCon2021优秀解题思路分享：物联网固件自动化漏洞挖掘WP （浙江大学 go-go-go战队）
contest: DataCon 2021
year: 2021
difficulty: hard
vuln_type: misc_unknown
tags: [iot, firmware, angr, def-use, symbols, pypy, 多架构, 污点分析]
attack_chain:
  - 用angr跨平台静态分析+PyPy即时编译
  - 危险函数表: popen/system/doSystemCmd/sprintf/snprintf/AES_cbc_encrypt等
  - 获取CFG+PLT段处理延迟绑定
  - ReachingDefinitionsAnalysis def-use链追踪
  - 参数只读地址段→确定不可利用
  - 命令注入: system前0x20字节sprintf+format不含%s
  - 密码学误用: IV/KEY需来自安全随机数
  - 调用路径DFS深度10：source func到sink func
key_payload: RDA.tracking=arg; if arg@ro: NOT_EXPLOITABLE
one_liner: DataCon2021物联网固件angr+def-use自动漏洞挖掘多架构
lesson: angr RDA+CFG可跨mips/arm/x86分析，PyPy加速
quality: high
---

# DataCon2021优秀解题思路分享：物联网固件自动化漏洞挖掘WP （浙江大学 go-go-go战队）

## 题目信息
- 比赛：DataCon 2021
- 方向：物联网固件自动化漏洞挖掘
- 战队：浙江大学 go-go-go

## 关键攻击链
### 1. 技术选型
- **angr** 跨平台静态分析 + 符号执行
- **PyPy** 即时编译器加速

### 2. 危险函数列表
- 命令注入：`popen / system / doSystemCmd / doSystembk / doSystem / _popen / _system`
- 密码学误用：`AES_set_encrypt_key / EVP_DecryptInit_ex / DES_set_key_checked / AES_cbc_encrypt`
- 格式化字符串：`sprintf / snprintf`

### 3. 危险函数检测
- 获取二进制 CFG
- PLT 延迟绑定机制：交叉引用可能在 PLT
- 排除 PLT 节点后前继节点 = 调用地址

### 4. 参数 def-use 链追踪
- `ReachingDefinitionsAnalysis` 模块
- 追踪到只读地址段 → 确定不可利用
- ARM 架构下 sprintf 第二参数 R1 指向只读 → 不可利用

### 5. 命令注入检测
- system 前 0x20 字节内 sprintf（确保 format 后是命令参数）
- 符号执行 block 起点到 system 调用地址
- 提取 format 字符串，不含 `%s` → 不可利用

### 6. 密码学误用
- IV / KEY 不能是常数
- AES_cbc_encrypt key 必须来自 AES_set_encrypt_key 输出

### 7. 函数调用路径
- source 函数 6 大类：外部输入/内存/文件/网络/环境/其他
- DFS 深度 10 搜索 source→danger 路径
- 有路径 → 不确定可利用

### 8. 特殊处理
- 符号表错位、混淆、mip32 延迟槽
- function handler：local function 二次 RDA
- external function 模拟

## 评分
- quality: high（angr + PyPy + 多架构 def-use + 污点分析完整框架）
