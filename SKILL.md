---
name: ctf-knowledge
description: 使用 Des-CTF-Knowledge 知识库解题。当用户给出 CTF 题目（Web/Crypto/Misc/Reverse/Pwn/Forensic）、需要漏洞利用 Payload、需要查找历史类似 WriteUp、需要跑现成解题脚本时使用。
---

# CTF 解题 Agent 协议

> 本文件是 agent 调用本知识库的**唯一入口**。不要试图通读全库（32MB，不可能塞进上下文）。

## 核心纪律

1. **先侦察再给方案**：在没有证据前，禁止输出 payload。
2. **每个结论带出处**：`文件:行号` 或 MCP 返回的 `source`。
3. **失败要反思**：观察到的信号命中 `traps/TRAPS-INDEX.md` 时，立刻怀疑当前方向。
4. **不确定就说不确定**：标注 confidence，不要编造 WP 或 flag。

## 五步循环

```
0. 信号   → 先查 techniques/TECHNIQUES.md（37 张卡）→ 未命中查 ATOMS.md（2432 条）
1. 侦察   → 提炼题面特征词（文件类型/报错/现象/关键字）
2. 搜索   → search("特征词")，或 find_wp(category, technique)
3. 假设   → "我猜这是 X 题，因为 ___"（写下来，标注 confidence）
4. 验证   → get_payload / run_script / read_topic 取具体证据
5. 复盘   → 失败时查 traps/TRAPS-INDEX.md 对应信号组
```

## 工具选择表

| 你现在想干什么 | 调用什么 |
|---|---|
| **观察到某个信号，想知道该用什么手法** | `find_technique(signal="栈溢出但没后门")` ← **第一步** |
| 上面没命中，想找长尾知识 | `find_atom("RSA n 是质数")` ← 2432 条技法原子 |
| 不知道这是什么题 | `search(题面关键词)` |
| 找历史上解过同类题的 WP | `find_wp(technique="反序列化")` |
| 要一个能直接用的 payload | `get_payload(vuln_type="sql_injection")` |
| 想读某类漏洞的完整原理 | `read_topic("SQL")` → 按返回的章节行号精读 |
| 要跑现成脚本 | `run_script("图片爆破宽高")` |
| 思路卡住了 | `find_technique(signal=你看到的现象)` / `search("失败", scope="traps")` |
| 想看某个大赛的所有题 | `find_wp(contest="KCTF", year=2023)` |

## 知识分三层，按这个顺序查

```
第 1 层  techniques/TECHNIQUES.md   37 张手写卡：signal + steps + traps
         ↓ 命不中
第 2 层  techniques/ATOMS.md        2432 条自动原子：一句话一条
         ↓ 命不中 / 需要题面佐证
第 3 层  CTF大赛WP集合/articles/    1049 篇原始 WP：降级为"证据"
```

**⚠️ 关键：先逆向拿证据，再查库。不要用题目描述查库。**

实测（见 [techniques/VALIDATION.md](techniques/VALIDATION.md)）：
用题目描述查库会把"名字带 imgz 的堆题"误判成图片隐写，把 PE 逆向误判成 ret2libc。
正确的查询输入是**证据**：

| ❌ 错误输入 | ✅ 正确输入 |
|---|---|
| "imgz 这题怎么做" | "导入 malloc free memcpy，.text 0x7272，非PIE" |
| "legacy_gateway 逆向" | "PE32 Windows 控制台，MFC 对话框，校验输入" |
| "图片打不开" | "PNG IHDR 宽高与 CRC 不符" |

**为什么 WP 降级为证据**：实测这批 WP 100% 图片被移除、57% 代码块换行被压平。
直接读 WP 容易抄到跑不通的代码。所以 —— **先拿技法，再用 WP 核对题面**，而不是先读 WP。

用原子时注意 `confidence`：
- `explicit`（25 条）：条件是真的，可直接判断适用性
- `derived`（2407 条）：条件是从题面推断的，**不构成充分条件，必须自己验证**

## 检索路径（无 MCP 时用）

```bash
# 1. 定位技术文章章节
python3 tools/gen_idx.py --check          # 索引是否新鲜
grep -n "^#" SQL.idx.md | grep 宽字节      # 找到行号
sed -n '928,935p' SQL.md                  # 精读该节

# 2. 找历史 WP（结构化字段，比全文 grep 准）
grep -l "^subcategory_guess: deserialization" CTF大赛WP集合/articles/*.md
grep -l "^contest_normalized: \"KCTF\"" CTF大赛WP集合/articles/*.md

# 3. 找踩过的坑
grep -A3 "被过滤/拦截" traps/TRAPS-INDEX.md
```

## 输出格式

```markdown
## 题目判断
- 类型: web/deserialization  (confidence: high)
- 依据: 源码里有 unserialize($_GET['d'])，且无 __wakeup 校验

## 攻击链
1. ...

## 可执行步骤
```bash
curl ...
```

## 出处
- PHP反序列化漏洞总结.md:264-547 (POP链)
- traps/TRAPS-INDEX.md#被过滤拦截 (同类失败案例)
```

## 禁止事项

- ❌ 没有 `search`/`read_topic` 证据就输出 payload
- ❌ 把 `failed_attempts` 里的"假设"当作事实
- ❌ 编造不存在的 WP 文件名或 flag
- ❌ 在靶场/授权环境外使用本库的利用代码
