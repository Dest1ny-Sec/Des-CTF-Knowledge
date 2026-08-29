---
title: 看雪2023 KCTF年度赛 | 第三题设计思路及解析
contest: 看雪2023 KCTF年度赛
year: 2023
difficulty: medium
vuln_type: reverse
tags: [SOUI界面, Resource Hacker, dlg_main.xml, CloseHandle异常反调试, CreateTimerQueueTimer 4个反调试, ARM代码验证, SHA256, 简单设计]
attack_chain: Resource Hacker提取dlg_main.xml→IDA WinMain找到simulation vftable偏移2a8→0x4078C5 CloseHandle((HANDLE)0x99999999)异常反调试→CreateTimerQueueTimer 4个反调试(NtSetInformationThread/NtQueryInformationProcess)→patch jz→jmp绕过→找到check_va按钮sub_406490→sub_405C50处理自定义消息0x47A-0x47E→sub_4061D0含明文+ARM代码SHA256验证
key_payload: "simulation::vftable偏移2a8;CloseHandle((HANDLE)0x99999999);4个CreateTimerQueueTimer;jz→jmp绕过反调试;sub_406490 check_va;sub_405C50 switch 0x47A-0x47E"
one_liner: KCTF2023年度赛Q3《秘密计划》SOUI界面+4个定时器反调试+ARM代码明文SHA256验证
lesson: SOUI界面逆向先提取dlg_main.xml定位vftable；定时器反调试patch jz→jmp绕过
quality: high
---

# 看雪2023 KCTF年度赛 | 第三题设计思路及解析

**赛事**：看雪2023 KCTF年度赛 Q3《秘密计划》

**难度**：6队破解

**题目设计**：
- GUI程序（SOUI框架）
- ARM代码中验证（无混淆无加密）
- ARM代码中**直接给出明文**
- 核心：SHA256值反推明文

**赛题解析**：

**Step 1：提取SOUI布局**
- Resource Hacker看资源 → 提取dlg_main.xml
- 主界面布局：input_va输入框 + check_va按钮

**Step 2：IDA找vftable**
- `simulation::vftable` 偏移 = 2a8
- 后面要用

**Step 3：反调试绕过**
- 0x4078C5: `CloseHandle((HANDLE)0x99999999)` 异常反调试
- 触发EXCEPTION_INVALID_HANDLE → 调试器捕获 → 应用处理 → 退出
- 正常执行不触发异常

**Step 4：定时器反调试**
- CreateTimerQueueTimer 4个反调试函数：
  - sub_407880：CloseHandle异常反调试
  - sub_407900：NtSetInformationThread 检测调试器
  - sub_4079D0：NtQueryInformationProcess 检测调试器
  - sub_407A60：Mutex反调试（A2D972DA-0A03-41D4-906B-6EFF73D0C937）
- **绕过**：0x406102处 `jz loc_406192` 改为 `jmp loc_406192`

**Step 5：消息处理**
- sub_405C50 switch 0x47A-0x47E 自定义消息
- sub_4061D0 提示字符串
- check_va按钮 → sub_405AF0 → sub_406490
- 后续 sub_405AF0 检测按钮名称

**Step 6：ARM代码验证**
- 验证核心在解密出来的ARM代码
- ARM代码简单（无混淆无加密）
- ARM代码中**直接给出明文**
- 等价于：根据SHA256值反推明文

**核心技术**：
- SOUI界面逆向（dlg_main.xml + vftable定位）
- 4种反调试技术（CloseHandle异常/SetInformationThread/QueryInformationProcess/Mutex）
- ARM代码明文对照
- 定时器反调试patch绕过

**质量评估**：高（完整反调试绕过流程）
