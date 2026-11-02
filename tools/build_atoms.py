#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_atoms.py — 从 WP 的 lesson 字段抽取"技法原子"。

设计取舍（重要）
    试过从 attack_chain 抽，失败：7900 条去重后 7875 条只出现一次，
    且内容是"这一题怎么做的"（如 add(0xc0,"X"*0x20) 写 ROP），
    几乎不含跨题复用信息 —— 做成 1000 个技法等于把 WP 换个格式重存。

    lesson 字段才是真知识：「任何RSA题都应先验证n是合数」、
    「IDA 静态看不出真实 key 时优先动态调试」—— 这是"何时用什么"。
    2457 条原子，中位数 36 字，粒度刚好。

signal 的来源（三层，由强到弱）
    1. explicit  原子本身含条件词（当/如果/优先/避免/不要...）→ 直接切出条件句
    2. derived   从所属 WP 的 title/one_liner/tags 反推触发场景
    3. domain    兜底：只给领域，不给假信号（宁可缺失也不编）

产出
    techniques/atoms.json  结构化，供 MCP
    techniques/ATOMS.md    人类可读

用法
    python3 tools/build_atoms.py
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
OUT_JSON = os.path.join(ROOT, "techniques", "atoms.json")
OUT_MD = os.path.join(ROOT, "techniques", "ATOMS.md")

# 条件/信号词
COND_WORDS = ["当", "如果", "若", "一旦", "见到", "出现", "遇到", "此时",
              "前提下", "才能", "才会", "适合", "优先", "不要", "避免",
              "注意", "警惕", "而非", "别只", "首先", "先"]

# 句子切分：分号 + 句号（但保留小数点和 0x 里的点）
SPLIT_RE = re.compile(r"[；;]|(?<=[\u4e00-\u9fff])。(?=[\u4e00-\u9fffA-Za-z])")

# 过滤：纯描述/无操作性的句子
JUNK_PAT = [
    re.compile(r"^(本题|该题|题目|这道题|这题)"),
    re.compile(r"^\d+\s*$"),
    re.compile(r"^(详见|参见|见上文|同上)"),
]

MIN_LEN = 12
MAX_LEN = 200


def extract_condition(atom):
    """从原子句里切出「触发条件」与「结论/动作」。

    中文习惯是「条件在前，结论在后」，且条件常以以下形态结尾：
      - 「...时」/「...的话」/「...时,」
      - 「当 X」/「若 X」/「如果 X」（前导词 + 从句）
      - 「X 若 Y」（从句在中间）

    返回 (condition, conclusion)。切不出时返回 (None, atom)。
    """
    # 形态 1：前导条件词，从句到首个逗号/句末
    for w in ("当", "如果", "若", "一旦", "遇到", "见到"):
        if atom.startswith(w):
            m = re.match(r"^(" + w + r".{2,80}?[，,。]|" + w + r".{2,80}?的话)", atom)
            if m:
                return m.group(1).strip("，,。"), atom[m.end():].strip() or atom
            return w, atom  # 整句都是条件

    # 形态 2：条件以「时」/「的话」结尾（最常见的中文结构）
    m = re.match(r"^(.{4,60}?(?:时|的话|情况下|前提)[，,。])", atom)
    if m:
        rest = atom[m.end():].strip()
        if len(rest) >= 6:
            return m.group(1).strip("，,。"), rest

    # 形态 3：句中「X 若 Y」
    m = re.match(r"^([^，,]{4,40})[，,](若|如果)(.{4,80})$", atom)
    if m:
        return m.group(1) + "，" + m.group(2) + m.group(3), atom

    return None, atom


def derive_signal(wp):
    """从 WP 元信息反推触发场景（derived 层）。"""
    parts = []
    if wp.get("one_liner"):
        parts.append(str(wp["one_liner"])[:60])
    tags = [str(t) for t in (wp.get("tags") or [])][:3]
    if tags:
        parts.append("标签: " + " / ".join(tags))
    return " | ".join(parts) if parts else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-sources", type=int, default=1,
                    help="至少被几篇 WP 提及（1=保留全部）")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(WP_DIR, "*.md")))
    atoms = {}
    stats = Counter()

    for p in files:
        b = open(p, "rb").read()
        if not b.startswith(b"---\n"):
            continue
        e = b.find(b"\n---\n", 4)
        if e < 0:
            continue
        try:
            d = yaml.safe_load(b[4:e + 1].decode("utf-8", "replace")) or {}
        except Exception:
            stats["bad_yaml"] += 1
            continue
        lesson = str(d.get("lesson") or "").strip()
        if len(lesson) < MIN_LEN:
            stats["no_lesson"] += 1
            continue

        for raw in SPLIT_RE.split(lesson):
            s = (raw or "").strip(" 　\n\t-*•")
            if len(s) < MIN_LEN:
                stats["too_short"] += 1
                continue
            if len(s) > MAX_LEN:
                s = s[:MAX_LEN].rstrip() + "…"
            if any(pat.search(s) for pat in JUNK_PAT):
                stats["junk"] += 1
                continue

            key = s
            if key in atoms:
                atoms[key]["sources"] = list(dict.fromkeys(
                    atoms[key]["sources"] + [os.path.basename(p)]))
                stats["merged"] += 1
                continue

            cond, body = extract_condition(s)
            conf = "explicit" if cond else "derived"
            atoms[key] = {
                "id": "a%04d" % (len(atoms) + 1),
                "atom": body if cond else s,
                "condition": cond,
                "signal_confidence": conf,
                "domain": str(d.get("category") or ""),
                "subcategory": str(d.get("subcategory_guess") or d.get("subcategory") or ""),
                "tags": [str(t) for t in (d.get("tags") or [])][:5],
                "derived_signal": derive_signal(d),
                "sources": [os.path.basename(p)],
                "contest": d.get("contest_normalized") or d.get("contest"),
                "year": d.get("contest_year") or d.get("year"),
            }
            stats["atoms"] += 1

    lst = [a for a in atoms.values() if len(a["sources"]) >= args.min_sources]
    # 给 confident 的排前面，其余按领域聚拢
    lst.sort(key=lambda a: ({"explicit": 0, "derived": 1}[a["signal_confidence"]],
                            a["domain"], a["id"]))

    by_domain = Counter(a["domain"] for a in lst)
    by_conf = Counter(a["signal_confidence"] for a in lst)

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    payload = {
        "generated_from": "CTF大赛WP集合/articles/*.md :: lesson",
        "total_atoms": len(lst),
        "by_domain": dict(by_domain),
        "by_signal_confidence": dict(by_conf),
        "atoms": lst,
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # Markdown
    L = []
    L.append("<!-- AUTO-GENERATED by tools/build_atoms.py — 请改源 WP 的 lesson 字段 -->")
    L.append("# ATOMS — 技法原子层")
    L.append("")
    L.append(f"从 {len(files)} 篇 WP 的 `lesson` 字段抽出 **{len(lst)}** 条技法原子。")
    L.append("")
    L.append("> **原子 vs 卡片**：`TECHNIQUES.md` 提供高频技法卡片（数量见该文件）（有完整 signal/steps/traps），")
    L.append("> 本文件是自动抽取的长尾覆盖（一句话一条）。agent 优先查卡片，命不中再查原子。")
    L.append("")
    L.append("> **`signal_confidence` 的含义**：")
    L.append("> - `explicit`：原子本身带条件词（当/如果/优先/避免），condition 可直接当触发条件")
    L.append("> - `derived`：条件是从所属 WP 的题面反推的，仅供参考，**不可当作充分条件**")
    L.append("")
    L.append("| 领域 | 原子数 |")
    L.append("|---|---|")
    for k, v in by_domain.most_common():
        L.append(f"| {k or '(未分类)'} | {v} |")
    L.append("")
    L.append(f"显式条件 {by_conf.get('explicit', 0)} 条 / 推断条件 {by_conf.get('derived', 0)} 条")
    L.append("")
    L.append("---")
    L.append("")

    cur = None
    for a in lst:
        if a["domain"] != cur:
            cur = a["domain"]
            L.append(f"## {cur or '(未分类)'}")
            L.append("")
        mark = "🎯" if a["signal_confidence"] == "explicit" else "·"
        L.append(f"- {mark} **`{a['id']}`** {a['atom']}")
        if a["condition"]:
            L.append(f"  - 条件：{a['condition']}")
        if a["signal_confidence"] == "derived" and a["derived_signal"]:
            L.append(f"  - 来源题面：{a['derived_signal'][:80]}")
        L.append(f"  - 出处：`{a['sources'][0]}`" +
                 (f" 等 {len(a['sources'])} 篇" if len(a["sources"]) > 1 else ""))
    L.append("")
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    print(f"原子总数: {len(lst)}")
    print(f"  显式条件(explicit): {by_conf.get('explicit', 0)}")
    print(f"  推断条件(derived):  {by_conf.get('derived', 0)}")
    print("  领域分布:", dict(by_domain))
    print(f"过滤统计: {dict(stats)}")
    print(f"✓ 已生成 {OUT_MD} 与 {OUT_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
