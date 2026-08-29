---
title: DataCon 2023漏洞分析赛题二官方题解
contest: DataCon 2023 漏洞分析
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [openwrt, codeql, joern, cypher, strcat, memmove, system, popen, odhcpd]
attack_chain:
  - OpenWrt源码魔改题目
  - 设置3种固定漏洞模式
  - 第一种: strcat第二参数是变量
  - match (n:identifier) where n.callee="strcat" and n.index=1
  - 第二种: memmove第三参数是变量且不基于size申请
  - match (n:identifier) where n.callee="memmove" and n.index=2
  - 第三种: system/popen第一参数是变量
  - 漏洞1+2: odhcpd
  - 0x000036A9 odhcpd
  - 0x000035F9
key_payload: match (n:identifier) where n.callee="strcat" and n.index=1
one_liner: DataCon 2023漏洞分析题二：OpenWrt魔改+CodeQL参数特征查询
lesson: CodeQL+Joern按callee+index查询是漏洞分析高效模式
quality: high
---

# DataCon 2023漏洞分析赛题二官方题解

## 题目信息
- 比赛：DataCon 2023
- 题目：漏洞分析赛题二
- 类别：OpenWrt 源码魔改
- 工具：CodeQL / Joern

## 关键攻击链
### 题目设计
- 来源：openwrt/openwrt 魔改
- 3 种固定漏洞模式
- 目标：探索静态分析工具 + 人工审计结合

### 漏洞模式 1：strcat 危险参数
```cypher
match (n:identifier) 
where n.callee = "strcat" and n.index = 1 
with [n] as taintPropagationPath 
RETURN taintPropagationPath
```
- strcat 第二参数 = 变量 → 可能溢出
- 结果：odhcpd 0x000036A9 和 0x000035F9

### 漏洞模式 2：memmove 危险参数
```c
void * memmove(void *dst, const void *src, size_t len);
```
- 安全用法 1：`memmove(dest, src, sizeof(dest))`（len 是常量）
- 安全用法 2：`dest = malloc(size); memmove(dst, src, size);`（按 len 申请）
- 危险：`len` 是变量且不基于 size 申请
- 查询：`n.callee="memmove" and n.index=2`

### 漏洞模式 3：system/popen 危险参数
- 第一参数是变量 → 命令注入
- 查询：`n.callee="system" or n.callee="popen" and n.index=0`

### 总结
- 实际固件上传后先查 system/popen
- 第一参数常量 → 不可能是命令注入
- 减轻人工逆向工作量

## 评分
- quality: high（CodeQL/Joern 完整查询模板 + 3 种漏洞模式总结）
