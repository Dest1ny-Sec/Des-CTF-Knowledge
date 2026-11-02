#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Des-CTF-Knowledge MCP Server

把知识库从"能被读"变成"能被调"。agent 通过工具调用检索，而不是靠自觉去读索引文件。

启动：
    python3 mcp/server.py            # stdio transport（Claude Desktop / Claude Code / Cursor）

工具：
    search          全文/结构化检索，返回 路径:行号 + 摘要
    read_topic      读某篇技术文章的指定章节（自动用 idx）
    find_wp         按 category/contest/year/technique 查历史 WP
    get_payload     按漏洞类型取可用 payload
    run_script      列出/执行 CTF常用脚本
    solve_hint      给题面描述，返回最相似的 WP + 攻击链
"""
import json
import os
import re
import subprocess
import sys
from collections import Counter

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WP_DIR = os.path.join(ROOT, "CTF大赛WP集合", "articles")
TRAPS_JSON = os.path.join(ROOT, "traps", "traps.json")
TECH_JSON = os.path.join(ROOT, "techniques", "techniques.json")
ATOMS_JSON = os.path.join(ROOT, "techniques", "atoms.json")
SCRIPTS_DIR = os.path.join(ROOT, "CTF常用脚本及工具")

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # 允许在无 MCP SDK 时直接跑自检
    FastMCP = None


# ---------------------------------------------------------------- 基础索引
def _load_wp_index():
    """启动时一次性加载所有 WP 的 frontmatter，供结构化过滤。"""
    idx = []
    if not os.path.isdir(WP_DIR):
        return idx
    for fn in sorted(os.listdir(WP_DIR)):
        if not fn.endswith(".md"):
            continue
        p = os.path.join(WP_DIR, fn)
        try:
            b = open(p, "rb").read()
            if not b.startswith(b"---\n"):
                continue
            e = b.find(b"\n---\n", 4)
            if e < 0:
                continue
            fm = yaml.safe_load(b[4:e + 1].decode("utf-8", "replace")) or {}
        except Exception:
            continue
        fm["_file"] = fn
        fm["_body_offset"] = b[:e + 5].decode("utf-8", "replace").count("\n") + 1
        idx.append(fm)
    return idx


WP_INDEX = _load_wp_index()


def _wp_record(fm):
    return {
        "file": fm.get("_file"),
        "title": fm.get("title"),
        "contest": fm.get("contest_normalized") or fm.get("contest"),
        "year": fm.get("contest_year") or fm.get("year"),
        "category": fm.get("category"),
        "subcategory": fm.get("subcategory_guess") or fm.get("subcategory"),
        "attack_chain": fm.get("attack_chain") or [],
        "one_liner": fm.get("one_liner"),
        "failed_attempts": fm.get("failed_attempts") or [],
        "lesson": fm.get("lesson"),
        "quality": fm.get("quality"),
    }


STOPWORDS = set("""
的 了 这 那 是 在 和 与 或 也 都 就 而 及 等 一个 我们 你 我 题目 给了 拿 到
需要 如何 怎么 什么 程序 服务 系统 实现 使用 内容 部分 情况 问题 方法 过程
给出 分析 处理 相关 一般 可以 时候 如果 但是 因为 所以 这个 那个
二进制 只有 判断 出现 大量 看到 发现 拿到 中看到 里面 样子 形式 类型
下面 上面 这里 那里 已经 还是 就是 不是
""".split())

# 高频但无区分度的 2-gram（多是跨词边界产物），一律丢弃
NOISE_BIGRAMS = set("""
二进 进制 制约 断有 判断 只有 出现 大量 看到 发现 拿到 给了 里面 下面 上面
这里 那里 已经 还是 就是 不是 可以 一个 我们 这个 那个 什么 怎么 如何 有的
""".split())

# 跨领域的歧义词：单独出现不足以定位领域，必须配合强锚词
AMBIGUOUS = {"溢出", "注入", "绕过", "攻击", "利用", "读取", "上传", "包含", "泄露", "截断"}

# 领域锚词：命中则提示 agent 该查哪个方向
DOMAIN_ANCHORS = {
    "web": ["sql", "xss", "ssrf", "ssti", "lfi", "rce", "upload", "反序列化", "命令执行",
            "文件包含", "文件上传", "waf", "webshell", "csrf", "xxe", "jwt", "原型链", "注入点"],
    "pwn": ["pwn", "rop", "tcache", "fastbin", "unsorted", "heap", "堆", "栈", "libc",
            "canary", "格式化字符串", "house of", "gadget", "shellcode", "内核提权"],
    "reverse": ["逆向", "反编译", "jadx", "ida", "混淆", "vm", "opcode", "apk", "so 文件"],
    "crypto": ["rsa", "aes", "des", "cbc", "ecc", "格", "lattice", "ecc", "哈希", "md5"],
    "misc": ["隐写", "png", "jpg", "pcap", "流量", "压缩包", "zip", "取证", "usb", "音频"],
}



def detect_domain(text):
    low = str(text or "").lower()
    best, bestn = None, 0
    for dom, keys in DOMAIN_ANCHORS.items():
        n = sum(1 for k in keys if k in low)
        if n > bestn:
            best, bestn = dom, n
    return best, bestn


def _tokens(text):
    """中英文混合分词：中文取 2-gram，英文按词。"""
    text = str(text or "").lower()
    toks = set()
    for w in re.findall(r"[a-z0-9_\.\-\+]{2,}", text):
        toks.add(w)
    zh = re.findall(r"[\u4e00-\u9fff]+", text)
    for seg in zh:
        if len(seg) == 1:
            toks.add(seg)
            continue
        for i in range(len(seg) - 1):
            g = seg[i:i + 2]
            if g not in STOPWORDS and g not in NOISE_BIGRAMS:
                toks.add(g)
        # 整段中文也要过停用词，否则"二进制""只有"这类会整段漏进来
        if 2 <= len(seg) <= 6 and seg not in STOPWORDS:
            toks.add(seg)
    return toks


def _score(query_tokens, doc_text):
    dt = _tokens(doc_text)
    if not dt or not query_tokens:
        return 0.0
    overlap = len(query_tokens & dt)
    return overlap / (len(query_tokens) ** 0.5)


# ---------------------------------------------------------------- 工具实现
def _search_impl(query, scope="all", limit=10):
    q_toks = _tokens(query)

    if scope == "docs":
        return _search_sections(q_toks, query, limit)

    hits = []

    # 索引类文件只做导航，不参与正文计分（否则 README/INDEX 永远排第一）
    NAV_FILES = {"README.md", "CHANGELOG.md", "AI-SEARCH-INDEX.md", "SKILL.md",
                 "PAYLOAD-CHEATSHEET.md"}

    if scope == "wp":
        for fm in WP_INDEX:
            blob = " ".join(str(fm.get(k)) for k in
                            ("title", "tags", "attack_chain", "key_observations",
                             "one_liner", "subcategory", "summary"))
            score = _score(q_toks, blob)
            if score > 0:
                r = _wp_record(fm)
                r["score"] = round(score, 2)
                r["kind"] = "wp"
                r["source"] = f"CTF大赛WP集合/articles/{r['file']}"
                hits.append(r)

    if scope == "traps":
        if os.path.exists(TRAPS_JSON):
            data = json.load(open(TRAPS_JSON, encoding="utf-8"))
            for sig in data.get("signals", []):
                for case in sig.get("cases", []):
                    blob = f"{case.get('attempt')} {case.get('reason')}"
                    score = _score(q_toks, blob)
                    if score > 0:
                        hits.append({"kind": "trap",
                                     "source": f"traps/TRAPS-INDEX.md#{sig['signal']}",
                                     "signal": sig["signal"],
                                     "when_to_doubt": sig.get("when_to_doubt"),
                                     "attempt": case.get("attempt"),
                                     "reason": case.get("reason"),
                                     "score": round(score, 2)})

    if scope == "all":
        domain, strength = detect_domain(query)
        # 纯歧义词查询（如"溢出"）不做强领域判断
        res = _search_sections(q_toks, query, limit, domain=domain, strength=strength)
        hits.extend(res["results"])
        wp = _search_impl(query, "wp", limit)
        hits.extend(wp["results"])
        tr = _search_impl(query, "traps", limit)
        hits.extend(tr["results"])

        # 领域权重：PWN/Reverse 的知识主要沉淀在 WP 里，技术文章覆盖弱
        if domain in ("pwn", "reverse") and strength >= 2:
            for h in hits:
                if h["kind"] == "wp":
                    h["score"] = round(h.get("score", 0) * 2.2, 2)
                elif h["kind"] == "section":
                    h["score"] = round(h.get("score", 0) * 0.7, 2)

    hits.sort(key=lambda h: -h.get("score", 0))
    return {"query": query, "count": len(hits), "results": hits[:limit],
            "domain_guess": detect_domain(query)[0]}


# ---- 章节级检索：把每篇技术文章按标题切块，按块打分 ----
_SECTION_CACHE = None


def _build_section_index():
    """把 12 篇技术文章 + PAYLOAD 按标题切成章节块。"""
    global _SECTION_CACHE
    if _SECTION_CACHE is not None:
        return _SECTION_CACHE
    blocks = []
    SECTION_FILES = [
        "SQL.md", "命令执行.md", "文件上传漏洞.md", "文件包含.md", "SSRF漏洞.md",
        "PHP反序列化漏洞总结.md", "php代码审计.md", "JWT.md", "SSTI.md",
        "图片隐写.md", "音频隐写.md", "压缩包总结.md", "PAYLOAD-CHEATSHEET.md",
        "CTF常用脚本及工具/SCRIPTS-INDEX.md", "traps/TRAPS-INDEX.md",
    ]
    files = []
    for rel in SECTION_FILES:
        if os.path.exists(os.path.join(ROOT, rel)):
            files.append(rel)
    # 靶场 WP 也切成章节
    for base in sorted(os.listdir(os.path.join(ROOT, "WP汇总"))) if os.path.isdir(os.path.join(ROOT, "WP汇总")) else []:
        p = os.path.join("WP汇总", base)
        if base.endswith(".md"):
            files.append(p)
    for fname in files:
        path = os.path.join(ROOT, fname)
        idx = os.path.join(ROOT, fname[:-3] + ".idx.md")
        lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
        if os.path.exists(idx):
            for line in open(idx, encoding="utf-8"):
                m = re.search(r"\[(.*?)\]\([^)]*\)\s*→\s*L(\d+)-L(\d+)", line.strip())
                if not m:
                    continue
                title, a, b = m.group(1), int(m.group(2)), int(m.group(3))
                body = "\n".join(lines[a - 1:b])
                blocks.append({"file": fname, "title": title, "L": f"{a}-{b}",
                               "body": body, "_toks": _tokens(title + " " + body[:2000])})
        else:
            # 无 idx 的文件：按 markdown 标题就地切块
            cur = None
            for i, l in enumerate(lines, 1):
                if l.startswith("#"):
                    if cur:
                        blocks.append(cur)
                    cur = {"file": fname, "title": l.lstrip("# ").strip(),
                           "L": f"{i}-{len(lines)}", "body": "", "_toks": set()}
                elif cur is not None:
                    cur["body"] += l + "\n"
            if cur:
                blocks.append(cur)
            # 回填 token 与末行号
            for k, b in enumerate(blocks):
                if b["file"] == fname and not b["_toks"]:
                    b["_toks"] = _tokens(b["title"] + " " + b["body"][:2000])
    _SECTION_CACHE = blocks
    return blocks


def _search_sections(q_toks, query, limit, domain=None, strength=0):
    blocks = _build_section_index()
    # 歧义词降权：避免"溢出"把 SQL 的 BigInt溢出排到堆溢出前面
    eff_toks = q_toks - AMBIGUOUS if len(q_toks - AMBIGUOUS) > 0 else q_toks
    scored = []
    for b in blocks:
        title_toks = _tokens(b["title"])
        t_hit = len(eff_toks & title_toks)
        b_hit = len(eff_toks & b["_toks"])
        if not t_hit and not b_hit:
            continue
        score = t_hit * 3.0 + b_hit * 0.6
        # 领域一致性：查 PWN 类关键词时，命中 web 文章要打压
        if domain and strength >= 2:
            file_dom, _ = detect_domain(b["title"] + " " + b["body"][:600])
            if file_dom and file_dom != domain:
                score *= 0.35
        scored.append({"kind": "section", "file": b["file"],
                       "source": f"{b['file']}:{b['L'].split('-')[0]}",
                       "section": b["title"], "L": b["L"],
                       "score": round(score, 2),
                       "snippet": _snippet(b["body"], query)})
    scored.sort(key=lambda h: -h["score"])
    return {"query": query, "count": len(scored), "results": scored[:limit]}


def _snippet(text, query, width=120):
    low = text.lower()
    i = low.find(query.lower())
    if i < 0:
        return text.strip()[:width]
    a = max(0, i - width // 3)
    return text[a:a + width].replace("\n", " ").strip()


def _read_topic_impl(topic, section=None):
    """读技术文章；topic 可为文件名或关键词，section 为章节名（模糊匹配 idx）。"""
    candidates = [f for f in os.listdir(ROOT)
                  if f.endswith(".md") and not f.endswith(".idx.md")
                  and f not in ("README.md", "CHANGELOG.md", "SKILL.md")]
    stem = topic[:-3] if topic.endswith(".md") else topic
    match = [f for f in candidates if stem.lower() in f.lower()]
    if not match:
        # 用 idx 标题反查
        best, bestn = None, 0
        for f in candidates:
            idx = os.path.join(ROOT, f[:-3] + ".idx.md")
            if not os.path.exists(idx):
                continue
            n = open(idx, encoding="utf-8").read().lower().count(stem.lower())
            if n > bestn:
                best, bestn = f, n
        if not best:
            return {"error": f"未找到主题 {topic!r}", "available": candidates}
        match = [best]
    fname = match[0]
    idx_path = os.path.join(ROOT, fname[:-3] + ".idx.md")

    if not os.path.exists(idx_path):
        return {"file": fname, "note": "无 idx，请直接读全文",
                "content": open(os.path.join(ROOT, fname), encoding="utf-8").read()[:4000]}

    entries = []
    for line in open(idx_path, encoding="utf-8"):
        # 兼容两种格式：
        #   -   [标题](SQL.md#anchor) → L6-L26
        #   - L1-L24: 旧式手写导航（无锚点，跳过）
        m = re.search(r"\[(.*?)\]\([^)]*\)\s*→\s*L(\d+)-L(\d+)", line.strip())
        if m:
            entries.append((m.group(1), int(m.group(2)), int(m.group(3))))

    if not entries:
        return {"file": fname,
                "error": f"{idx_path} 不是新格式（缺少 → Lx-Ly 条目）。请运行 python3 tools/gen_idx.py"}  
    lines = open(os.path.join(ROOT, fname), encoding="utf-8", errors="replace").read().split("\n")
    if section:
        sel = [e for e in entries if section.lower() in e[0].lower()]
        if not sel:
            return {"file": fname, "error": f"未找到章节 {section!r}",
                    "sections": [{"title": t, "L": f"{a}-{b}"} for t, a, b in entries]}
        chunks = []
        for title, a, b in sel:
            chunks.append(f"### {title} (L{a}-L{b})\n" + "\n".join(lines[a - 1:b]))
        return {"file": fname, "matched_sections": [e[0] for e in sel],
                "content": "\n\n".join(chunks)}

    return {"file": fname, "total_lines": len(lines),
            "sections": [{"title": t, "L": f"{a}-{b}"} for t, a, b in entries],
            "hint": "传入 section 参数读取具体章节"}


def _find_wp_impl(category=None, contest=None, year=None, technique=None, limit=15):
    res = []
    for fm in WP_INDEX:
        if category and str(fm.get("category")) != category:
            continue
        cn = str(fm.get("contest_normalized") or "")
        if contest and contest.lower() not in cn.lower():
            continue
        cy = fm.get("contest_year") or fm.get("year")
        if year and str(cy) != str(year):
            continue
        if technique:
            blob = " ".join(str(fm.get(k)) for k in
                            ("title", "one_liner", "summary", "subcategory",
                             "subcategory_guess", "tags", "attack_chain"))
            if technique.lower() not in blob.lower():
                continue
        res.append(_wp_record(fm))
    return {"count": len(res), "results": res[:limit],
            "facets": {
                "category": dict(Counter(str(f.get("category")) for f in WP_INDEX)),
                "top_contests": dict(Counter(str(f.get("contest_normalized")) for f in WP_INDEX).most_common(15)),
            }}


def _get_payload_impl(vuln_type):
    p = os.path.join(ROOT, "PAYLOAD-CHEATSHEET.md")
    text = open(p, encoding="utf-8").read()
    lines = text.split("\n")
    # 找最近的二级标题包含该类型的块
    start = None
    aliases = {
        "sql": "SQL注入", "sqli": "SQL注入", "sql_injection": "SQL注入",
        "xss": "XSS", "ssti": "SSTI", "rce": "命令执行", "cmd": "命令执行",
        "upload": "文件上传", "lfi": "文件包含", "xxe": "XXE",
        "ssrf": "SSRF", "jwt": "JWT", "deserialize": "反序列化", "反序列化": "反序列化",
    }
    key = aliases.get(vuln_type.lower(), vuln_type)
    for i, l in enumerate(lines):
        if l.startswith("## ") and key.lower() in l.lower():
            start = i
            break
    if start is None:
        heads = [l for l in lines if l.startswith("## ")]
        return {"error": f"未找到 {vuln_type}", "available": heads}
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return {"vuln_type": vuln_type, "section": lines[start], "content": "\n".join(lines[start:end])}


def _run_script_impl(name, args=None, execute=False):
    if not name:
        dirs = []
        for d in sorted(os.listdir(SCRIPTS_DIR)):
            fp = os.path.join(SCRIPTS_DIR, d)
            if os.path.isdir(fp):
                files = [f for f in os.listdir(fp) if f.endswith(".py")]
                if files:
                    dirs.append({"name": d, "scripts": files})
        return {"count": len(dirs), "scripts": dirs}
    target = os.path.join(SCRIPTS_DIR, name)
    if not os.path.isdir(target):
        cand = [d for d in os.listdir(SCRIPTS_DIR) if name in d]
        return {"error": f"未找到脚本目录 {name!r}", "candidates": cand}
    pys = sorted(f for f in os.listdir(target) if f.endswith(".py"))
    out = {"directory": name, "scripts": pys}
    if execute and pys:
        cmd = [sys.executable, os.path.join(target, pys[0])] + (args or [])
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=target)
            out["executed"] = pys[0]
            out["stdout"] = r.stdout[-4000:]
            out["stderr"] = r.stderr[-2000:]
            out["returncode"] = r.returncode
        except subprocess.TimeoutExpired:
            out["error"] = "执行超时 60s"
    else:
        out["hint"] = "execute=True 可运行主脚本（注意：多数脚本需自行改 URL/参数）"
    return out


_TECH_CACHE = None


def _load_techniques():
    global _TECH_CACHE
    if _TECH_CACHE is None:
        if os.path.exists(TECH_JSON):
            _TECH_CACHE = json.load(open(TECH_JSON, encoding="utf-8")).get("techniques", [])
        else:
            _TECH_CACHE = []
    return _TECH_CACHE


NEG_MARK = ("没结果", "没有结果", "无结果", "没用", "无效", "失败", "不成功",
            "打不开", "跑不出", "没找到", "无输出", "不通", "打不通", "跑不通",
            "被拦", "没反应", "不生效", "不work", "不行")

# 明确是"技法主题"的词：即使出现在否定句里也不剔除（它们是用户想解决的问题，不是被否定的方法）
TOPIC_KEEP = {"phar", "ssrf", "ssti", "lfi", "jwt", "xss", "xxe", "rce", "sql",
              "反序列化", "文件包含", "文件上传", "命令执行", "栈溢出", "堆溢出",
              "gopher", "dict", "zsteg", "binwalk", "base64"}


# 领域兼容：PWN 与 REVERSE 常重叠；MISC 含取证/隐写
DOMAIN_COMPAT = {
    ("pwn", "reverse"): True, ("reverse", "pwn"): True,
    ("misc", "forensic"): True, ("forensic", "misc"): True,
    ("ai-agent", "web"): True, ("ai-agent", "crypto"): True,
    ("ai-agent", "misc"): True, ("ai-agent", "reverse"): True,
}


def _domain_compatible(card_dom, ev_dom, text):
    """卡片领域是否与证据领域相容。"""
    if card_dom == ev_dom:
        return True
    if DOMAIN_COMPAT.get((card_dom, ev_dom)):
        return True
    # 证据里明确提到该卡片的领域词时放行
    t = (text or "").lower()
    hint = {"web": ["http", "url", "cookie", "注入", "ssrf", "xss", "反序列化"],
            "pwn": ["栈", "堆", "libc", "rop", "gets", "read("],
            "reverse": ["pe", "windows", "ida", "反编译", "opcode", "vm"],
            "crypto": ["rsa", "aes", "密文", "密钥"],
            "misc": ["隐写", "取证", "流量", "压缩"],
            "ai-agent": ["模型", "oracle", "mcp", "agent", "预算"]}
    return any(k in t for k in hint.get(card_dom, []))


# 技术栈互斥：查询提到某栈时，其他栈的卡降权
STACK_HINTS = {
    "java": ["java", "classpath", "commonsbeanutils", "commonscollections",
             "templatesimpl", "jdbcrowset", "fastjson", "objectinputstream", "readobject"],
    "php": ["php", "unserialize", "phar", "call_user_func", "preg_match", "thinkphp", "laravel"],
    "python": ["python", "pickle", "flask", "jinja", "django", "pyinstaller"],
    "node": ["node", "javascript", "prototype pollution", "__proto__", "npm", "ejs"],
}
STACK_CARD_TAG = {
    "java": ["java", "commonsbeanutils", "commonscollections", "templatesimpl",
             "jdbcrowset", "fastjson", "ysoserial"],
    "php": ["php", "phar", "unserialize", "call_user_func", "preg_match"],
    "python": ["python", "pickle", "flask", "jinja", "django", "pyinstaller"],
    "node": ["node", "javascript", "__proto__", "ejs", "npm"],
}


def _lang_compat_penalty(signal, card, kw_blob, sig_blob):
    """在 _find_technique_impl 里就地修改 score，用返回值体现。"""
    t = (signal or "").lower()
    blob = (kw_blob + " " + sig_blob).lower()
    for stack, hints in STACK_HINTS.items():
        if not any(h in t for h in hints):
            continue
        own = STACK_CARD_TAG.get(stack, [])
        if any(o in blob for o in own):
            continue          # 该卡属于这个栈，不罚
        # 卡属于别的栈 → 罚
        other = [o for st, tags in STACK_CARD_TAG.items() if st != stack for o in tags]
        if any(o in blob for o in other):
            return 0.25
    return 1.0


def _negated_tools(text):
    """识别「某工具/手法 被否定」的语境，返回被否定的关键词列表。

    例："图片能打开但 zsteg 没结果" -> ['zsteg']
        "试了 base64 没用"          -> ['base64']
    """
    t = str(text or "")
    out = []
    for mark in NEG_MARK:
        i = t.find(mark)
        if i < 0:
            continue
        head = t[max(0, i - 20):i]
        for tok in re.findall(r"[A-Za-z0-9_][A-Za-z0-9_.+-]{1,20}", head):
            out.append(tok.lower())
        # 中文工具/手法名（2-6 字）
        for tok in re.findall(r"[\u4e00-\u9fff]{2,6}", head):
            out.append(tok)
    # 主题词不剔除：用户说"phar 打不通"是在问 phar 怎么打通，不是在否定 phar 这个技法。
    # 但像 gopher / zsteg / base64 这种「具体子手法」被否定时，应降低它在打分里的作用，
    # 所以这里仍返回它们，由调用方决定是剔除还是降权。
    return out


def _find_technique_impl(signal=None, domain=None, technique_id=None, limit=5,
                         reviewed_only=False):
    """按「观察到的信号」检索技法卡片——这是原子层的核心入口。"""
    cards = _load_techniques()
    if technique_id:
        hit = [c for c in cards if c.get("id") == technique_id]
        return {"count": len(hit), "results": hit}

    out = []
    q = _tokens(signal) if signal else set()
    # 从证据里推断领域；若卡片领域与证据领域冲突，重罚（不排除，留作候选）
    ev_domain, ev_strength = detect_domain(signal or "")
    # 关键：被否定的工具/手法，从查询 token 里剔除 —— 用户是在说"这个方法没用"，
    # 再拿它去匹配"用这个方法的卡片"没有意义。
    if signal:
        for neg in _negated_tools(signal):
            if len(neg) >= 3 and neg.lower() not in TOPIC_KEEP:
                q = {t for t in q if neg not in t}
        # 被否定的 TOPIC_KEEP 词降权而非剔除：保留主题，但不让"子手法"主导排序
        for neg in _negated_tools(signal):
            if neg.lower() in TOPIC_KEEP:
                pass  # 由卡片级惩罚处理
    for c in cards:
        if domain and c.get("domain") != domain:
            continue
        if reviewed_only and (c.get("review_status") or "unreviewed") in ("unreviewed",):
            continue
        # 分桶打分：keywords >> signal/name >> steps
        # 中文 2-gram 下「读取」「绕过」这类词到处都是，必须让 keywords 主导
        kw_blob = " ".join(str(x) for x in (c.get("keywords") or []))
        sig_blob = " ".join([str(c.get("name") or ""), str(c.get("signal") or ""),
                             str(c.get("signal_en") or ""), str(c.get("distinguish") or "")])
        step_blob = " ".join(str(x) for x in (c.get("steps") or []))
        score = 0.0
        if q:
            kw_hits = len(q & _tokens(kw_blob))
            sig_hits = len(q & _tokens(sig_blob))
            step_hits = len(q & _tokens(step_blob))
            # keywords 命中权重是 steps 的 6 倍
            score = kw_hits * 3.0 + sig_hits * 1.2 + step_hits * 0.5

            # 领域冲突惩罚：证据明显是 PE/Windows/堆，就不该首推 ret2libc 这类 ELF 栈题卡
            if ev_strength >= 2 and ev_domain and c.get("domain"):
                cd = c.get("domain")
                if cd != ev_domain and not _domain_compatible(cd, ev_domain, signal):
                    score *= 0.2

            # 语言/技术栈互斥：查询明确提到 Java 时，PHP/Python 专属卡不应胜出
            score *= _lang_compat_penalty(signal, c, kw_blob, sig_blob)

            # 「X 没结果 / X 无效 / X 失败」= 该工具已试过没用。
            # 若卡片的关键词完全依赖被否定的工具（该工具是它的唯一特征），直接跳过这张卡；
            # 否则大幅降权。
            negs = [n for n in _negated_tools(signal) if len(n) >= 3]
            if negs:
                kw_l = kw_blob.lower()
                hit_negs = [n for n in negs if n in kw_l]
                if hit_negs:
                    kw_list = [str(x).lower() for x in (c.get("keywords") or [])]
                    only_negated = all(
                        any(n in k for n in hit_negs) for k in kw_list if k
                    ) and len(kw_list) <= 3
                    if only_negated:
                        continue        # 整张卡就建立在这个被否定的工具上 → 跳过
                    score *= 0.25
                elif any(n in sig_blob.lower() for n in negs):
                    score *= 0.4
        else:
            score = 0.1
        if score <= 0:
            continue
        st = c.get("review_status") or "unreviewed"
        out.append({
            "id": c.get("id"), "name": c.get("name"), "domain": c.get("domain"),
            "signal": c.get("signal"), "steps": c.get("steps"), "traps": c.get("traps"),
            "auto_traps": [t["case"] for t in (c.get("auto_traps") or [])],
            "evidence_count": c.get("evidence_count"),
            "evidence": (c.get("evidence") or [])[:5],
            "review_status": st,
            "review_notes": c.get("review_notes"),
            "score": round(score, 2),
        })

    # 审核状态作为 tie-breaker：同分时 verified > corrected > unreviewed > unverified
    REVIEW_RANK = {"verified": 0, "corrected": 1, "unreviewed": 2, "unverified": 3}
    out.sort(key=lambda x: (-x["score"], REVIEW_RANK.get(x.get("review_status"), 2)))
    return {"count": len(out), "results": out[:limit]}


_ATOM_CACHE = None


def _load_atoms():
    global _ATOM_CACHE
    if _ATOM_CACHE is None:
        if os.path.exists(ATOMS_JSON):
            _ATOM_CACHE = json.load(open(ATOMS_JSON, encoding="utf-8")).get("atoms", [])
        else:
            _ATOM_CACHE = []
    return _ATOM_CACHE


def _find_atom_impl(query, domain=None, explicit_only=False, limit=10):
    """在 2400+ 技法原子中检索。

    与 find_technique 的区别：
      find_technique = 37 张精写卡，有完整 signal/steps/traps，优先用
      find_atom      = 长尾覆盖，一句话一条，signal_confidence 需自行判断
    """
    atoms = _load_atoms()
    q = _tokens(query)
    out = []
    for a in atoms:
        if domain and a.get("domain") != domain:
            continue
        if explicit_only and a.get("signal_confidence") != "explicit":
            continue
        blob = " ".join([str(a.get("atom") or ""), str(a.get("condition") or ""),
                         str(a.get("derived_signal") or ""),
                         " ".join(a.get("tags") or [])])
        score = _score(q, blob)
        if score <= 0:
            continue
        # 显式条件的原子加权——它们能直接判断适用性
        if a.get("signal_confidence") == "explicit":
            score *= 1.5
        out.append({
            "id": a.get("id"), "atom": a.get("atom"),
            "condition": a.get("condition"),
            "confidence": a.get("signal_confidence"),
            "domain": a.get("domain"), "subcategory": a.get("subcategory"),
            "derived_signal": a.get("derived_signal"),
            "source": (a.get("sources") or [None])[0],
            "n_sources": len(a.get("sources") or []),
            "score": round(score, 2),
        })
    out.sort(key=lambda x: -x["score"])
    return {"query": query, "count": len(out), "results": out[:limit],
            "note": "confidence=derived 的条件是从题面推断的，不构成充分条件，需自行验证"}


def _solve_hint_impl(description, limit=5):
    r = _search_impl(description, scope="wp", limit=limit)
    traps = _search_impl(description, scope="traps", limit=3)
    tech = _find_technique_impl(signal=description, limit=3)
    atoms = _find_atom_impl(description, limit=3)
    return {"description": description,
            "matched_techniques": tech["results"],
            "matched_atoms": atoms["results"],
            "similar_wp": r["results"],
            "relevant_traps": traps["results"]}


# ---------------------------------------------------------------- MCP 注册
def build_server():
    mcp = FastMCP("des-ctf-knowledge")

    @mcp.tool()
    def search(query: str, scope: str = "all", limit: int = 10) -> dict:
        """检索知识库。scope: all|docs|wp|traps。返回带 文件:行号 的命中，可直接用于引用。"""
        return _search_impl(query, scope, limit)

    @mcp.tool()
    def read_topic(topic: str, section: str = "") -> dict:
        """读取技术文章。topic 为文件名或关键词(如 SQL / 反序列化 / JWT)。
        section 为空时返回章节目录+行号；给出 section 时返回该章节正文。"""
        return _read_topic_impl(topic, section or None)

    @mcp.tool()
    def find_wp(category: str = "", contest: str = "", year: str = "",
                technique: str = "", limit: int = 15) -> dict:
        """按结构化字段查历史 WP。category: web/misc/pwn/reverse/crypto/forensic。
        contest: 归一化大赛名(如 KCTF/强网杯)。technique: 关键词(如 deserialization)。"""
        return _find_wp_impl(category or None, contest or None, year or None,
                             technique or None, limit)

    @mcp.tool()
    def get_payload(vuln_type: str) -> dict:
        """取某类漏洞的高频 payload 速查段。vuln_type: sql/xss/ssti/rce/upload/lfi/xxe/ssrf/jwt/反序列化。"""
        return _get_payload_impl(vuln_type)

    @mcp.tool()
    def run_script(name: str = "", args: list | None = None, execute: bool = False) -> dict:
        """列出/执行 CTF 解题脚本。name 为空时列出全部脚本目录。
        execute=True 会实际运行（默认关闭，避免误执行）。"""
        return _run_script_impl(name, args, execute)

    @mcp.tool()
    def find_technique(signal: str = "", domain: str = "", technique_id: str = "",
                       limit: int = 5, reviewed_only: bool = False) -> dict:
        """按观察到的"信号"检索技法卡片（技能原子层）。
        signal: 你观察到的现象，如"响应长度稳定但内容不同"。
        domain: web/pwn/crypto/reverse/misc/ai-agent。
        technique_id: 已知卡片 id 时直接取（如 t010-ret2libc）。"""
        return _find_technique_impl(signal or None, domain or None,
                                    technique_id or None, limit, reviewed_only)

    @mcp.tool()
    def find_atom(query: str, domain: str = "", explicit_only: bool = False,
                  limit: int = 10) -> dict:
        """在 2432 条技法原子里检索（长尾知识，一句话一条）。
        先用 find_technique（37 张精写卡），命不中再查这里。
        explicit_only=True 只返回带显式条件词的原子（可靠但少）。"""
        return _find_atom_impl(query, domain or None, explicit_only, limit)

    @mcp.tool()
    def solve_hint(description: str, limit: int = 5) -> dict:
        """输入题面描述，返回最相似的历史 WP 攻击链 + 相关失败陷阱。"""
        return _solve_hint_impl(description, limit)

    return mcp


def main():
    if FastMCP is None:
        print("缺少 mcp SDK：pip install mcp", file=sys.stderr)
        return 1
    build_server().run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
