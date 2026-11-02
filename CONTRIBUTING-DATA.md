# 贡献与数据规范

> 面向：想往本库补充内容的人、想把本库接入自己系统的人。
> 先读 [DATA-QUALITY.md](DATA-QUALITY.md) 了解数据现状与缺陷。

---

## 一、目录结构

```
.
├── CTF大赛WP集合/articles/     1049 篇大赛 WP（一题一文件，标准 frontmatter）
├── WP汇总/                     靶场 WP（ctfshow / upload-labs / SQLI-LABS）
├── *.md                        12 篇漏洞专题文章（带 .idx.md 分段索引）
├── PAYLOAD-CHEATSHEET.md       10 大类 payload 速查
├── CTF常用脚本及工具/           50+ 解题脚本 + SCRIPTS-INDEX.md
├── techniques/
│   ├── cards/*.yaml            ★ 技法卡片（人工编写，质量最高）
│   ├── TECHNIQUES.md           卡片汇总（自动生成）
│   ├── ATOMS.md / atoms.json   技法原子 2432 条（从 lesson 自动抽取）
│   └── VALIDATION.md           有效性验证报告
├── traps/                      失败案例库 2863 条（本库最差异化资产）
├── mcp/                        MCP server（给 agent 用，非必需）
├── tools/                      清洗 / 生成 / 校验脚本
└── exports/                    导出数据集（gitignored）
```

---

## 二、WP 数据字典

每篇 WP = YAML frontmatter + Markdown 正文。

### 必填字段

| 字段 | 类型 | 说明 | 示例 |
|---|---|---|---|
| `title` | str | 题目/文章标题 | `2022 RCTF WriteUp by Venom` |
| `contest` | str | 原始赛事名（保留原样） | `RCTF 2022` |
| `contest_normalized` | str | **归一化赛事名**（用于检索） | `RCTF` |
| `contest_year` | int | 赛事年份 | `2022` |
| `category` | str | 方向 | `web` / `pwn` / `crypto` / `misc` / `reverse` / `forensic` |
| `subcategory` | str | 子类 | `sql_injection` / `heap_exploitation` |
| `attack_chain` | **list** | 攻击步骤（**必须列表，不能是字符串**） | `['抓包', '发现越权', '读 flag']` |
| `lesson` | str | **一句话经验**（最有价值，原子层来源） | `弱口令优先于漏洞` |

### 推荐字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `tags` | list | 技术标签，用于聚类检索 |
| `one_liner` | str | 一句话概括 |
| `failed_attempts` | list | **失败尝试**（格式 `尝试X → 失败：原因`） |
| `key_observations` | list | 关键观察 |
| `subcategory_guess` | str | `*_other` 桶的启发式归类 |
| `flag_observed` | list | 真实可验证的 flag |
| `source_url` | str | 原文链接（必须保留，尊重版权） |
| `quality` | str | `high` / `medium` |

### ⚠️ 常见错误

**1. `attack_chain` 写成字符串**

```yaml
# ❌ 错：下游无法按步骤遍历
attack_chain: 抓包 → 发现越权 → 读 flag

# ✅ 对
attack_chain:
- '抓包'
- '发现越权'
- '读 flag'
```

**2. YAML 特殊字符未转义**

```yaml
# ❌ 错：含 % 或 : 或引号会破坏 YAML 结构
keywords: [格式化字符串, %n]
lesson: 先判 a,c: 用公式

# ✅ 对
keywords: [格式化字符串, "%%n"]
lesson: '先判 a,c：用公式'
```

**3. 用 NUL 字节**

原始抓取内容里可能带 `\x00`，会让 `grep` 把文件判为二进制而**静默跳过**。
提交前跑 `python3 tools/sanitize_corpus.py --dry-run` 检查。

---

## 三、三种使用场景

### 场景 A：建 RAG 知识库（推荐）

```bash
python3 tools/export_dataset.py --format rag --out exports/
# → exports/rag_corpus.jsonl  一行一篇 {id, content, metadata}
```

- 每条带 `quality_issues`（`code_newlines_flattened` / `fence_unbalanced`），
  下游可据此降权
- 建议分块 1000-1500 tokens，重叠 200
- 检索时优先查 `techniques/` 和 `traps/`，它们是纯文本、无图片依赖

### 场景 B：继续预训练（CPT）语料

```bash
python3 tools/export_dataset.py --format cpt --out exports/
# → exports/cpt_corpus.txt  约 23.5M 字符
```

- 适合让模型熟悉 CTF 术语与中文表达
- 建议先过滤 `very_short` 和 `code_newlines_flattened`

### 场景 C：监督微调（SFT）—— 有限可用

```bash
python3 tools/export_dataset.py --format sft --out exports/
# → exports/sft_dataset.jsonl  1784 条
```

**重要**：本库 78% 的 WP 无可验证 flag，22% 有题面。
所以 SFT 不是「题面→答案」，而是：

| kind | 条数 | 形式 |
|---|---|---|
| `step_pair` | 1571 | 观察步 → 应对步 |
| `step_to_flag` | 213 | 末步 → flag + 经验 |

**教的是「看到这个现象该怎么做」**。若你需要「题面→答案」范式，
本库不提供，需另找带附件和验证脚本的题库。

### 场景 D：给 agent 用（可选）

```bash
pip install mcp pyyaml
python3 mcp/server.py       # MCP stdio
```

⚠️ 见 [techniques/VALIDATION.md](techniques/VALIDATION.md)：
**必须用逆向证据查库，不能用题目描述查库**，否则会误判。

---

## 四、提交前检查清单

```bash
python3 tools/sanitize_corpus.py --dry-run    # NUL / 围栏
python3 tools/fix_attack_chain.py --dry-run   # attack_chain 类型
python3 tools/normalize_frontmatter.py --dry-run
python3 tools/gen_idx.py                     # 重建索引
python3 tools/build_techniques.py            # 技法层
python3 tools/build_atoms.py                 # 原子层
python3 tools/build_traps.py                 # 陷阱库
python3 tools/selfcheck.py                   # 13 项健康检查
```

全部通过再提交。CI 也会跑这些。

---

## 五、版权与来源

- 12 篇专题文章、脚本：MIT License
- WP 文章：来源于互联网公开渠道（主要 ctfiot.com），**版权归原作者**
- **不要删除 `source_url` 字段**——它是溯源的唯一凭据
- 若原作者要求下架，请提 Issue

---

## 六、贡献高质量内容的最佳方式

按价值排序：

1. **补充 `lesson` 字段**（一句话经验）—— 直接进入原子层，收益最大
2. **补充 `failed_attempts`**（`尝试X → 失败：原因`）—— 进入陷阱库
3. **新增技法卡片** `techniques/cards/*.yaml` —— 需含 signal/steps/traps
4. **新增 WP** —— 注意图片和代码块完整性
5. 修正错别字/失效链接

**最没价值的**：补充更多同质化 WP。本库不缺数量，缺的是「什么时候该怀疑自己」这类经验。
