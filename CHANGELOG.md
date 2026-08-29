# Changelog

## 索引

| 版本 | 日期 | 摘要 |
|---|---|---|
| v2.0.0 | 2026-08-29 | **重构**: 1156 篇原文 WP 抽取为 11 字段结构化 meta（`title/contest/year/difficulty/vuln_type/tags/attack_chain/key_payload/one_liner/lesson/quality`）。仓库 35MB → 5.4MB。AI-SEARCH-INDEX.md/README/ctf-solver.md 全部指向 `*.meta.md` |
| v1.0.0 | 2026-08-18 | 1156 篇 WriteUp 内容库首发 |
| v2026.5.30 | 2026-05-30 | 1156 篇 WP 格式批量修复：空行压缩 + HTML 清理 + 代码块空行恢复 + 空代码块清理 |

## 内容统计

- 漏洞深度文章：**12 篇**（SQL注入 / RCE / 文件上传 / 文件包含 / SSRF / SSTI / JWT / PHP反序列化 / PHP代码审计 / 命令执行 / 隐写术 / 流量分析）
- 历年大赛 WriteUp：**1156 篇结构化 meta**（强网杯 / 西湖论剑 / 网鼎杯 / HITCON / SECCON / N1CTF / RCTF / 长城杯 / 羊城杯 等 386 场大赛；v1.0.0 仍保留原文）
- Payload 速查：**10 大类**高频
- 解题脚本：**50+**（Base / RSA / CRC / USB流量 / 盲水印 / 古典密码 / steghide 等）
- 靶场 WP：ctfshow 全系列 + SQLI-LABS + upload-labs

## 贡献

本仓库是**内容**仓库，不是软件项目。Issues 主要用于：
- 🐛 WP 格式错乱
- 📝 内容勘误
- 💡 缺失的漏洞类型 / 大赛 WP

欢迎 PR 提交新内容（保持 Markdown 格式 + 文件名归类到对应子目录）。
