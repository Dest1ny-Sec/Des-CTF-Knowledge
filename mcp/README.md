# MCP Server — 让 agent 直接调用知识库

> 把知识库从「能被读」变成「能被调」。agent 不再需要「自觉」去读索引文件，
> 而是像调用函数一样检索：`search("宽字节注入")` → 直接拿到 `SQL.md:1473`。

---

## 快速开始

```bash
# 1. 安装依赖（唯一依赖）
pip install mcp pyyaml

# 2. 启动（stdio 传输，供桌面/CLI agent 使用）
python3 mcp/server.py
```

## 接入配置

### Claude Desktop / Claude Code

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）
或 `%APPDATA%\Claude\claude_desktop_config.json`（Windows）：

```json
{
  "mcpServers": {
    "des-ctf-knowledge": {
      "command": "python3",
      "args": ["/绝对路径/Des-CTF-Knowledge-latest/mcp/server.py"]
    }
  }
}
```

### Claude Code（项目级）

在项目根目录 `.mcp.json`：

```json
{
  "mcpServers": {
    "des-ctf-knowledge": {
      "command": "python3",
      "args": ["./mcp/server.py"]
    }
  }
}
```

### Cursor / 其他兼容 MCP 的客户端

同样的 `command` + `args` 即可，协议是标准的 MCP stdio。

---

## 工具清单

| 工具 | 用途 | 典型调用 |
|---|---|---|
| `search` | 章节级检索（标题加权 + 领域感知） | `search("宽字节注入")` |
| `read_topic` | 按章节读技术文章 | `read_topic("SQL", "宽字节")` |
| `find_wp` | 结构化查历史 WP | `find_wp(technique="deserialization")` |
| `get_payload` | 取某类漏洞 payload | `get_payload("sql")` |
| `run_script` | 列出/执行解题脚本 | `run_script("CRC32校验爆破")` |
| `solve_hint` | 题面 → 相似 WP + 相关陷阱 | `solve_hint("PNG 打不开")` |

### `search` 的 scope

- `docs`：12 篇技术文章 + PAYLOAD + SCRIPTS-INDEX + traps + 靶场 WP，**切成 1600+ 章节块**打分
- `wp`：1027 篇大赛 WP，按 frontmatter 字段打分
- `traps`：2863 条失败尝试
- `all`：混合排序，带 `domain_guess`

### 返回结构

```json
{
  "kind": "section",
  "source": "SQL.md:1473",
  "section": "宽字节注入",
  "L": "1473-1499",
  "score": 18.0,
  "snippet": "利用条件: ..."
}
```

agent 可直接用 `source` 做引用，用 `L` 做精读范围。

---

## 设计要点

1. **章节级而非文档级**：整篇文章切片太粗，一次命中会淹没细节。
   实测把 12 篇文章切成 570 个章节块、算上脚本索引共 1607 块后，
   「宽字节注入」能精确命中 `SQL.md:1473` 而不是整篇 SQL.md。

2. **领域感知排序**：中文 2-gram 会让「溢出」同时匹配 SQL 的「BigInt溢出」
   和 PWN 的「堆溢出」。通过原子领域锚词 + 跨领域降权解决。

3. **PWN/Reverse 走 WP**：这两类知识主要沉淀在 WP 里，技术文章覆盖弱，
   命中领域后自动给 WP 加权 2.2 倍。

4. **执行默认关闭**：`run_script` 的 `execute=False` 是默认值，
   避免 agent 误跑需要改 URL 的脚本。

---

## 自检

```bash
python3 tools/selfcheck.py
```
