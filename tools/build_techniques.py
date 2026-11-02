#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_techniques.py — 构建"技能原子层"。

为什么需要原子层
    WP 是一道题的全过程记录（题目特有的文件名、端口、赛题参数），
    直接喂给 agent 噪声很大。真正的可复用知识是**技法**：
    「什么信号下 → 用什么手法 → 具体步骤 → 哪些坑」

    WP 数量乘不上，但技法数量是有限的（本库 1027 篇 WP 里真正独立的技法约 60-90 个）。
    原子层把 N 篇 WP 压成 1 张卡片，agent 检索卡片即可，命中后再看具体 WP。

数据来源（全部自动，不手写）
    techniques/cards/*.yaml   人工编写的卡片骨架（signal / steps / traps 的初稿）
    CTF大赛WP集合/articles/*.md  frontmatter：自动回填 evidence（哪些 WP 用过这个技法）、
                                failed_attempts（自动补 traps）、attack_chain（自动补 steps）

产出
    techniques/TECHNIQUES.md   给 agent 读的总表（按领域分组）
    techniques/techniques.json 结构化版本，供 MCP

用法
    python3 tools/build_techniques.py            # 构建
    python3 tools/build_techniques.py --check    # 只报告覆盖率
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
OUT_MD = os.path.join(ROOT, "techniques", "TECHNIQUES.md")
OUT_JSON = os.path.join(ROOT, "techniques", "techniques.json")

FIELDS = ("id", "name", "domain", "signal", "signal_en", "steps", "traps",
          "tools", "keywords", "distinguish", "confidence",
          "review_status", "reviewed_at", "review_notes")


def load_cards():
    cards = []
    if not os.path.isdir(CARD_DIR):
        return cards
    for p in sorted(glob.glob(os.path.join(CARD_DIR, "*.yaml"))):
        try:
            c = yaml.safe_load(open(p, encoding="utf-8"))
        except Exception as ex:
            print(f"⚠ 跳过 {p}: {ex}", file=sys.stderr)
            continue
        if not isinstance(c, dict) or "id" not in c:
            continue
        c["_file"] = os.path.basename(p)
        for f in FIELDS:
            c.setdefault(f, [] if f in ("steps", "traps", "tools", "keywords") else "")
        cards.append(c)
    return cards


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


def _norm(s):
    return str(s or "").lower()


# 卡片领域 -> WP category 的映射（部分技法跨领域）
DOMAIN_TO_CATS = {
    "web": {"web"},
    "pwn": {"pwn"},
    "crypto": {"crypto"},
    "reverse": {"reverse"},
    "misc": {"misc", "forensic"},
    "ai-agent": {"web", "misc", "crypto", "reverse"},
}

# 过于通用的关键词：命中它们不足以认定技法，必须配一个专有关键词
GENERIC_KWS = {
    "system", "bypass", "绕过", "泄露", "隐写", "注入", "攻击", "利用", "rce",
    "vm", "crc", "lsb", "shellcode", "payload", "flag", "脚本", "读取", "解析",
    "libc", "stack", "heap", "aes", "rsa", "xor", "base64",
}


def _hits(kws, blob):
    """返回命中的关键词，区分专属词与泛词。"""
    specific = [k for k in kws if k in blob and k not in GENERIC_KWS and len(k) >= 3]
    generic = [k for k in kws if k in blob and (k in GENERIC_KWS or len(k) < 3)]
    return specific, generic


def match_wp(card, wp):
    """判断一篇 WP 是否用到这个技法。

    规则（收紧后）：
      1. 领域必须匹配（防止 ret2libc 卡吃到 web 题）
      2. 需要至少 1 个专属关键词命中，或 2 个泛关键词命中
    """
    kws = [_norm(k) for k in card.get("keywords") or [] if str(k).strip()]
    if not kws:
        return False

    dom = card.get("domain") or ""
    cats = DOMAIN_TO_CATS.get(dom)
    wp_cat = str(wp.get("category") or "")
    if cats and wp_cat not in cats:
        return False

    blob = " ".join([
        _norm(wp.get("subcategory")), _norm(wp.get("subcategory_guess")),
        " ".join(_norm(t) for t in (wp.get("tags") or [])),
        " ".join(_norm(s) for s in (wp.get("attack_chain") or [])),
        _norm(wp.get("title")), _norm(wp.get("one_liner")),
    ])
    specific, generic = _hits(kws, blob)
    required = card.get("required_keywords") or []
    if required and not any(_norm(k) in blob for k in required):
        return False
    if len(specific) >= 1:
        return True
    return len(generic) >= 3


def build(cards, wps):
    idx = []
    for c in cards:
        evid = [w for w in wps if match_wp(c, w)]
        # 自动补 traps（来自命中 WP 的 failed_attempts，取与技法关键词相关的）
        # 只收录与该技法**专属关键词**相关的失败案例，避免把无关的坑塞进来
        kws = [_norm(k) for k in c.get("keywords") or []
               if _norm(k) not in GENERIC_KWS and len(str(k)) >= 3]
        auto_traps = []
        seen = set()
        for w in evid:
            for fa in (w.get("failed_attempts") or []):
                fa_s = str(fa)
                fa_n = _norm(fa_s)
                if not any(k in fa_n for k in (c.get("required_keywords") or kws)):
                    continue
                key = fa_s[:60]
                if key in seen:
                    continue
                seen.add(key)
                auto_traps.append({"case": fa_s[:160], "source": w["_file"]})
                if len(auto_traps) >= 5:
                    break
            if len(auto_traps) >= 5:
                break

        entry = {f: c.get(f) for f in FIELDS}
        entry["review_status"] = c.get("review_status") or "unreviewed"
        entry.update({
            "id": c.get("id"),
            "evidence": [w["_file"] for w in evid],
            "evidence_count": len(evid),
            "auto_traps": auto_traps,
            "domains": dict(Counter(str(w.get("category")) for w in evid)),
        })
        idx.append(entry)

    idx.sort(key=lambda x: (-x["evidence_count"], x["id"]))
    return idx


def render_md(idx, coverage):
    L = []
    L.append("<!-- AUTO-GENERATED by tools/build_techniques.py — 请改 techniques/cards/*.yaml -->")
    L.append("# TECHNIQUES — 技能原子层")
    L.append("")
    L.append(f"{len(idx)} 张技法卡片，覆盖 {coverage['covered_wps']}/{coverage['total_wps']} 篇 WP"
             f"（{coverage['coverage_pct']}%）。")
    L.append("")
    L.append("> **为什么需要这一层**：WP 记录的是「这道题怎么做的」，")
    L.append("> 技法卡片记录的是「**什么信号出现时，该用什么手法**」——后者才是 agent 可复用的。")
    L.append("> 命中卡片后再去读 `evidence` 里的 WP 看具体题面。")
    L.append("")
    L.append("## 怎么用")
    L.append("")
    L.append("```")
    L.append("1. 观察到一个信号（如「响应长度稳定但内容不同」）")
    L.append("2. 在本表搜这个信号 → 命中技法卡片")
    L.append("3. 读卡片的 steps 照做；读 traps 避开已知坑")
    L.append("4. 需要题面参考时，打开 evidence 列的 WP")
    L.append("```")
    L.append("")
    L.append("---")
    L.append("")

    by_domain = defaultdict(list)
    for t in idx:
        by_domain[t.get("domain") or "other"].append(t)

    for dom in sorted(by_domain):
        L.append(f"## {dom}")
        L.append("")
        for t in by_domain[dom]:
            L.append(f"### `{t['id']}` {t['name']}")
            L.append("")
            if t.get("signal"):
                L.append(f"**信号**：{t['signal']}")
                L.append("")
            if t.get("distinguish"):
                L.append(f"**区分**：{t['distinguish']}")
                L.append("")
            if t.get("steps"):
                L.append("**步骤**：")
                for i, s in enumerate(t["steps"], 1):
                    L.append(f"{i}. {s}")
                L.append("")
            if t.get("traps"):
                L.append("**坑**：")
                for s in t["traps"]:
                    L.append(f"- {s}")
                L.append("")
            if t.get("auto_traps"):
                L.append("**来自 WP 的真实失败案例**：")
                for at in t["auto_traps"]:
                    L.append(f"- {at['case']}")
                L.append("")
            if t.get("tools"):
                L.append("**工具**：" + " · ".join(f"`{x}`" for x in t["tools"]))
                L.append("")
            if t.get("evidence"):
                shown = t["evidence"][:6]
                more = len(t["evidence"]) - len(shown)
                L.append(f"**证据**（{t['evidence_count']} 篇）：" +
                         " · ".join(f"`{e}`" for e in shown) +
                         (f" …等 {more} 篇" if more > 0 else ""))
                L.append("")
            L.append("---")
            L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    cards = load_cards()
    wps = load_wps()
    if not cards:
        print("尚无技法卡片（techniques/cards/*.yaml），请先添加", file=sys.stderr)
        return 1

    idx = build(cards, wps)

    covered = set()
    for t in idx:
        covered.update(t["evidence"])
    coverage = {
        "total_wps": len(wps),
        "covered_wps": len(covered),
        "coverage_pct": round(100 * len(covered) / max(len(wps), 1), 1),
        "cards": len(idx),
        "zero_evidence_missing": [t["id"] for t in idx if t["evidence_count"] == 0],
        "review_status": dict(Counter(str(t.get("review_status")) for t in idx)),
    }

    print(f"卡片 {len(idx)} 张 | 有证据 {len(idx) - len(coverage['zero_evidence_missing'])} | "
          f"零证据(待补关键词) {len(coverage['zero_evidence_missing'])}")
    print(f"WP 覆盖率: {coverage['covered_wps']}/{coverage['total_wps']} ({coverage['coverage_pct']}%)")
    if coverage["zero_evidence_missing"]:
        print("  零证据卡片:", ", ".join(coverage["zero_evidence_missing"][:12]))

    if args.check:
        return 0

    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(render_md(idx, coverage))
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump({"coverage": coverage, "techniques": idx}, f, ensure_ascii=False, indent=2)
    print(f"✓ 已生成 {OUT_MD} 与 {OUT_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
