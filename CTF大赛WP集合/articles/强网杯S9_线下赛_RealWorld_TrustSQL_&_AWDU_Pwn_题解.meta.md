---
title: 强网杯S9线下赛 RealWorld TrustSQL + AWDU Pwn 题解
contest: 强网杯S9线下赛(Real World)
year: 2025
difficulty: hard
vuln_type: web_unknown
tags: [SQLite3, EDITOR环境变量, system命令注入, format string, sqlite3扩展函数, 加固绕过, AWDU, AI_WAF, TrustSQL, sqlite3.51.0, 2025-11-04, system, gnome-calculator, x86_64, sqlite_create_function]
attack_chain: 静态分析SQLite3扩展函数:edit(1,1)+edit(2,1)=vuln函数 → 写temp%llx文件 + sprintf(env_1, filename) → system("%s \"%s\"", env_1, filename) → 设置EDITOR=gnome-calculator;. 触发edit(任意输入)→ 弹计算器 → 绕过AWDU AI WAF → 弹shell
key_payload: EDITOR环境变量+system命令注入+gnome-calculator弹计算器
one_liner: 强网杯S9线下赛 RealWorld TrustSQL:SQLite3扩展函数+EDITOR环境变量+system命令注入+弹计算器。
lesson: SQLite3自定义函数漏洞:edit(1)+edit(2)注册为vuln → 写文件到temp%llx → sprintf(env_1=EDITOR, filename) → system("EDITOR \"filename\"") → EDITOR=gnome-calculator;. → 任意命令执行;绕过AWDU AI WAF常见:执行特定字符串被识别,可拼接无害命令如ls/cat绕过。
quality: high
---
