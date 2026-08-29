---
title: 2026春节领红包 解题过程 纯手工分析（第八题、第十题未解出
contest: 春节活动
year: 2026
difficulty: hard
vuln_type: reverse
tags: [python312-pyc, IDA-real_main, PyLong, PyTuple, PyUnicode, len-validation, wasm-loader, UPX-mislabel, MCP-tool-chain, audit-flow]
attack_chain: 题目1 IDA 单步跟入 sub_7FFDBF84D9B0 → sub_7FFC5E78DC90 → sub_7FFC5E78A9B0 → sub_7FFC5E76B340 → sub_7FFC5E783A00 → real_main 调 printstrfunc 排冗 + 多次 false/true 验证（最终 v112 后 access denied）→ len 30 验证 → for 循环逐字符获取 flag（第一位 5 之后递归）/题目9 winrar 强开 CM1 发现 UPX 壳/题目8 wasm 加载 IDA9.3 报错 / jeb5.36 加载 wasm 失败/题目10 MCP 工具链：get_audit_log → _audit_token → update_tool_chain access_token → get_document secret:/board/resolutions → flag
key_payload: flag 第一位 5  长度 30  python312__Py_FalseStruct
one_liner: 2026 春节 hhxxhg 纯手工 WP，覆盖 Python 3.12 pyc 逆向、WASM 加载、MCP 工具链审计流。
lesson: Python 3.12 pyc 用 IDA 跟入 real_main 排冗后通过逐字符获取是有效路径；wasm 加载失败时需用工具栈 jeb5.36/IDA9.3 组合；MCP 工具链审计流需要按顺序执行 get_audit_log → update_tool_chain → execute_tool_chain → get_document。
quality: high
---

# 【2026春节领红包】解题过程，纯手工分析

## 概览
hhxxhg 的 2026 春节 5 道题纯手工分析 WP，含 Python 3.12 pyc 逆向、WASM、MCP 工具链审计流。

## 题目1 (Python 3.12 pyc 逆向)
- IDA 单步跟入 `sub_7FFDBF84D9B0` → `sub_7FFC5E78DC90` → `sub_7FFC5E78A9B0` → `sub_7FFC5E76B340` → `sub_7FFC5E783A00`
- 在 sub_7FFC5E783A00 中进入函数指针，找到主函数 `real_main` (sub_7FFC5E769C50)
- real_main 第一个参数传给其他函数，假设是 python 库的上下文结构体
- `printstrfunc` 相当于 Python print
- 第三个参数包含 PyUnicode 结构体的 PyTuple，PyUnicode 字符串跟在元数据后

### 验证流程
- `python312__Py_FalseStruct` 被 `get_bool_val` 处理为 0（多次假验证 + 真验证）
- 找到输出 v112 后出现 Access Denied，定位真验证
- 第一个调用返回 PyLong，分析后是字符串长度函数
- `totlen1` 长度变量，内存查得 30
- 输入 `123456789012345678901234567890`（长度 30）触发 for 循环
- 循环中第三个参数是 PyUnicode，获取的是正确 flag 字符
- 第一位 5，改为 `523456789012345678901234567890` 再次调试，依次获取每位
- 拼接完整 flag

## 题目9 (CM1 PE)
- 任务说明.html 有 "这不是 Web 题，没有额外的彩蛋、线索哦"
- IDA 打开 CM1 提示可能压缩
- stud_pe 查壳无结果
- winrar 强开发现是 UPX 壳

## 题目8 (WASM)
- jeb5.36 demo 版能加载 wasm 汇编码但反汇编失败
- IDA 9.3 列出 wasm 加载器但加载报 param type 错误
- WebAssembly 线性内存 = 连续可增长字节数组
  - load/store 系列：i32.load / i64.store / f32.load
  - 存放堆数据、数组、字符串、JS 共享缓冲区
- 表 = 间接函数调用存储
  - table.get / table.set / call_indirect
  - 实现语言运行时虚函数表
- 局部变量和操作数栈：local.get / local.set / global.get / global.set
- gen 函数开头几行汇编代码量巨大，F12 难翻阅

## 题目10 (MCP 工具链)
- guide 提示 review_template 对应 review_notes
- doc_id 用 review_doc_id 的 `confidential:/audit/logs` 执行 → access_token
- compliance_blob_b64 + compliance_note 提示 "chain_config 仅提交 get_audit_log"
- 在 get_audit_log 和 update_tool_chain 之间，后者报错才出现 "ctf" 字样
- 按"玄堂复核提示"，required_public_clues 列表执行 get_document，注意新会话不能只访问 secret:/board/resolutions
- 拿到 review_document 工具，参数 review_notes
- 之后 update_tool_chain / execute_tool_chain
- 先 get_audit_log 拿 _audit_token
- 填 update_tool_chain 的 access_token 参数
- 再以 _audit_token 作 access_token + secret:/board/resolutions 作 doc_id 执行 get_document → flag

## 经验提炼
- Python 3.12 pyc 用 IDA 跟入 real_main 是经典逆向路径
- 多次 false 验证 + 一次 true 验证要逐个加断点排查
- WASM 加载失败时需工具栈组合：jeb5.36 (demo 限制) + IDA9.3 (param type bug)
- MCP 工具链审计流：get_audit_log → update_tool_chain → execute_tool_chain → get_document
- 工具链调用的"顺序约束"和"组合约束"是 MCP 类题目核心考点
- winrar 强开 PE 文件可绕过 stud_pe 误判查壳
