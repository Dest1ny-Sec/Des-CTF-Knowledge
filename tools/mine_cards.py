#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mine_cards.py — 从现有 WP 挖掘「值得做成技法卡」的主题。

为什么需要
    手写卡只能覆盖我知道的技术。但 1049 篇 WP 里埋着大量我没见过的技术
    （如 House of Emma、Prettier RCE、kernel PCX），这些才是本库相对
    公开资料的真正增量。

做法（不靠猜，靠统计）
    1. 从每篇 WP 的 tags / attack_chain / lesson / failed_attempts 里抽技术术语
    2. 按「出现在多少篇不同 WP」排序 —— 跨题出现 = 可复用 = 值得成卡
    3. 与现有卡片比对，输出「未覆盖的高频术语」
    4. 对被丢弃的候选给出原因（已在卡里 / 太泛 / 太具体）

产出
    techniques/MINE-CANDIDATES.md    待写卡片清单（按证据量排序）

用法
    python3 tools/mine_cards.py
    python3 tools/mine_cards.py --min 3      # 至少 3 篇证据
"""
import argparse
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WP_DIR = os.path.join(ROOT, "CTF大赛WP集合", "articles")
CARD_DIR = os.path.join(ROOT, "techniques", "cards")
OUT = os.path.join(ROOT, "techniques", "MINE-CANDIDATES.md")

# 太泛的词：出现再多也不值得单独成卡
GENERIC = {
    "pwn", "web", "crypto", "misc", "reverse", "forensic", "ctf", "wp", "flag",
    "python", "java", "linux", "windows", "payload", "exploit", "shellcode",
    "shell", "command", "file", "read", "write", "system", "stack", "heap",
    "buffer", "overflow", "patch", "debug", "analysis", "script", "tool",
    "远程", "漏洞", "题目", "脚本", "分析", "利用", "环境", "服务",
    # 结构性/通用词，不是技术
    "admin", "password", "token", "cookie", "input", "delete", "index", "login",
    "user", "data", "test", "code", "name", "type", "value", "size", "offset",
    "http", "https", "request", "response", "server", "client", "socket",
    # 十六进制/编码碎片
    "x00", "x10", "x20", "x40", "x7f", "xff", "x100", "x90", "xdead", "xbeef",
    "ascii", "utf", "hex", "base", "delta",
    # 库/工具常用名（太泛）
    "p64", "u64", "p32", "u32", "read", "printf", "popen", "system", "execve",
    "gadget", "leak", "call", "size", "main", "init", "plt", "got", "bss",
}

# subcategory 占位值不是术语
SUBCAT_ARTIFACT = {"misc_other", "web_other", "pwn_other", "crypto_other",
                   "reverse_other", "forensic_other"}

# 允许成卡的纯字母技术词（人工白名单，避免噪声）
TECH_WORDS = {
    "canary", "tcache", "fastbin", "unsorted", "largebin", "houseof", "ollvm",
    "angr", "unicorn", "frida", "jadx", "qiling", "mprotect", "setcontext",
    "coppersmith", "lattice", "wiener", "paddingoracle", "mt19937", "lfsr",
    "xxtea", "rc4", "ssti", "ssrf", "xxe", "deserialize", "unserialize",
    "prototype", "jwt", "bkcrack", "zsteg", "steghide", "exiftool", "volatility",
    "dangerous", "obfuscation", "deobfuscation", "packer", "upx", "vmprotect",
}

# 已知的专有技术名（多词短语，直接保留）
PHRASE_RE = re.compile(r"[A-Za-z][A-Za-z0-9_\-]{2,}(?:\s+[A-Za-z][A-Za-z0-9_\-]{2,}){0,3}")
# 缩写/驼峰命名：HouseOfApple / ret2libc / OLLVM
CMPD_RE = re.compile(r"[A-Za-z]+(?:[0-9]+[A-Za-z]+|[A-Z][a-z]+)+|[a-z]+[0-9]+[a-z]+")


def load_cards():
    """返回 {已覆盖关键词集合, 卡片 id 列表}"""
    kws = set()
    ids = []
    for p in glob.glob(os.path.join(CARD_DIR, "*.yaml")):
        try:
            d = yaml.safe_load(open(p, encoding="utf-8")) or {}
        except Exception:
            continue
        ids.append(d.get("id", os.path.basename(p)))
        for k in (d.get("keywords") or []):
            kws.add(str(k).lower().strip())
        # name 里的英文也视为已覆盖
        for w in PHRASE_RE.findall(str(d.get("name") or "")):
            kws.add(w.lower())
    return kws, ids


def load_wps():
    out = []
    for f in sorted(glob.glob(os.path.join(WP_DIR, "*.md"))):
        b = open(f, "rb").read()
        if not b.startswith(b"---\n"):
            continue
        e = b.find(b"\n---\n", 4)
        if e < 0:
            continue
        try:
            d = yaml.safe_load(b[4:e + 1].decode("utf-8", "replace")) or {}
        except Exception:
            continue
        d["_file"] = os.path.basename(f)
        out.append(d)
    return out


def terms_of(wp):
    """从一篇 WP 抽取技术术语。"""
    parts = []
    parts += [str(t) for t in (wp.get("tags") or [])]
    ch = wp.get("attack_chain")
    if isinstance(ch, list):
        parts += [str(x) for x in ch]
    elif isinstance(ch, str):
        parts.append(ch)
    parts.append(str(wp.get("lesson") or ""))
    parts.append(str(wp.get("subcategory") or ""))
    parts += [str(x) for x in (wp.get("failed_attempts") or [])]
    blob = " ".join(parts)

    found = set()
    for m in PHRASE_RE.findall(blob):
        w = m.strip()
        low = w.lower()
        if len(low) < 3 or low in GENERIC:
            continue
        # 纯常见英文单词过滤（无技术含义）
        if low.isalpha() and len(low) < 5:
            continue
        if low in SUBCAT_ARTIFACT:
            continue
        # 排除编码碎片与数学表达式
        if re.match(r"^[xu][0-9a-f]*$", low):        # x28 / u64
            continue
        if re.match(r"^[a-z]-\d+$", low):            # p-1 / q-1
            continue
        if re.match(r"^x[0-9a-f]{4,}$", low):        # x9e3779b9
            continue
        if low.startswith("__") or low.endswith("__"):  # init__ / builtins__
            continue
        if re.match(r"^[0-9a-f]{6,}$", low):         # 纯 hex 串
            continue
        # 必须是"技术味"的：含数字/连字符，或是已知技术词表
        if not re.search(r"[0-9_\-/]", low) and low not in TECH_WORDS:
            continue
        found.add(low)
    for m in CMPD_RE.findall(blob):
        low = m.lower()
        if len(low) >= 4 and low not in GENERIC:
            found.add(low)
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=int, default=3, help="最少证据篇数")
    args = ap.parse_args()

    covered, card_ids = load_cards()
    wps = load_wps()

    ev = defaultdict(list)          # term -> [wp_file]
    for wp in wps:
        for t in terms_of(wp):
            ev[t].append(wp["_file"])

    def is_covered(term):
        if term in covered:
            return True
        for k in covered:
            if term in k or k in term:
                return True
        return False

    cands = []
    for term, files in ev.items():
        n = len(files)
        if n < args.min:
            continue
        if is_covered(term):
            continue
        cands.append((n, term, files))

    cands.sort(key=lambda x: (-x[0], x[1]))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    L = []
    L.append("<!-- AUTO-GENERATED by tools/mine_cards.py — 这是待写卡片的候选清单 -->")
    L.append("# MINE-CANDIDATES — 从现有 WP 挖出的待写卡片")
    L.append("")
    L.append(f"扫描 **{len(wps)}** 篇 WP，现有 **{len(card_ids)}** 张卡片。")
    L.append(f"下表是出现 ≥{args.min} 篇、但**尚未被任何卡片覆盖**的技术术语。")
    L.append("")
    L.append("> **为什么看这个表**：跨多篇 WP 反复出现 = 可复用 = 值得成卡。")
    L.append("> 尤其是那些公开资料里没有的（本库独有），价值最高。")
    L.append("")
    L.append("| 证据篇数 | 术语 | 示例来源 |")
    L.append("|---|---|---|")
    for n, term, files in cands:
        ex = files[0][:46]
        L.append(f"| **{n}** | `{term}` | {ex} |")
    L.append("")

    L.append("## 建议优先成卡的主题（证据最多的前 20）")
    L.append("")
    for n, term, files in cands[:20]:
        L.append(f"### `{term}`（{n} 篇）")
        L.append("")
        for f in files[:5]:
            L.append(f"- {f}")
        L.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    print(f"扫描 {len(wps)} 篇 WP / {len(card_ids)} 张卡")
    print(f"未覆盖的高频术语（≥{args.min} 篇）: {len(cands)}")
    print("\nTop 20 候选：")
    for n, term, files in cands[:20]:
        print(f"  {n:3} 篇  {term}")
    print(f"\n✓ 已生成 {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
