---
title: HITCON CTF 2022 EaaS
contest: HITCON CTF 2022
year: 2022
difficulty: hard
vuln_type: heap_exploit
tags: [pwn, python, fitz, buffer-overflow, pie-disabled, canary-disabled, partial-overwrite, pop-pop-pop-ret]
attack_chain:
  - Python fitz Document.save() 缓冲区溢出
  - Python PIE禁用+fitz.so canary禁用
  - 返回地址覆盖：每字节0x00-0x7f
  - 不能写null字节（结尾自动追加）
  - partial overwrite到pymain_repl
  - pop pop pop... ret gadget
  - Document.save() option参数放目标地址
  - 1/16或1/4096概率竞猜gadget
key_payload: pop pop pop... ret + pymain_repl
one_liner: HITCON CTF 2022 EaaS：Python fitz缓冲区溢出+partial overwrite
lesson: partial overwrite到pymain_repl进入交互模式
quality: high
---

# HITCON CTF 2022 EaaS

## 题目信息
- 比赛：HITCON CTF 2022
- 题目：EaaS（3/430 队解出）
- 分数：421

## 关键攻击链
### 1. 漏洞
- `Document.save()` 在 Python `fitz` 包有缓冲区溢出漏洞

### 2. 保护
- Python 二进制 PIE 禁用
- fitz.so canary 禁用
- 可覆盖返回地址

### 3. 写入限制
- 每个字节必须在 0x00-0x7f 范围
- 否则会被编码
- 不能写 null 字节
- 字符串结尾自动追加 null

### 4. 攻击思路
- 只能 partial overwrite 返回地址
- 跳转到原地址附近的 gadget
- Python 二进制 PIE 禁用是好目标
- 跳转到 Python 交互模式 `pymain_repl`
- [参考](https://github.com/python/cpython/blob/d291a82df33cd8c917a374fef2a2373beda78b77/Modules/main.c#L543)

### 5. 绕过限制
- 使用 `Document.save()` 的 option 参数
- option 放在栈上作为参数
- option 包含目标地址
- partial overwrite 返回地址到 `pop pop pop... ret` gadget
- 1/16 或 1/4096 概率

## 评分
- quality: high（Python 缓冲区溢出 + partial overwrite + pymain_repl 思路）
