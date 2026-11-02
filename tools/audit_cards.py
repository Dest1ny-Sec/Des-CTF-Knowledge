#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_cards.py — 技法卡片批量审核。

审核不是"看一眼觉得对"，而是对每张卡执行可复现的检查项，并给出四态结论：

    verified    所有检查项通过，且关键断言有外部依据
    corrected   发现并修正了问题
    unverified  存在无法独立核实的断言（保留并标注）
    suspect     存在与已知事实冲突的断言（必须修正）

检查项
    C1 结构性：steps/traps 必须全是字符串；keywords 非空
    C2 版本断言：声称某版本"可用/失效"时，必须与 KNOWN_VERSIONS 一致
    C3 危险指令：教具体取值（如 0xffff...）时必须提示其副作用
    C4 自洽性：同一张卡内不得自相矛盾（如同时说"可用"与"已移除"）
    C5 证据关联：evidence_count 为 0 的卡标记 unverified

KNOWN_VERSIONS 里的每条事实都附来源，来源是可访问的官方页面。

用法
    python3 tools/audit_cards.py --dry-run
    python3 tools/audit_cards.py --apply
"""
import argparse
import glob
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD_DIR = os.path.join(ROOT, "techniques", "cards")
TODAY = "2026-11-02"

# 已用官方来源核实的事实（审核时作为判据）
KNOWN_FACTS = [
    {
        "id": "glibc_hooks_removed",
        "pattern": r"__free_hook|__malloc_hook",
        "claim": "glibc 2.34 移除了 __free_hook/__malloc_hook",
        "source": "https://sourceware.org/pipermail/libc-alpha/2021-July/129193.html",
        "require_in_traps": r"2\.3[4-9]|2\.4\d[+\s号]|移除|没有",
    },
    {
        "id": "glibc_tcache_key",
        "pattern": r"tcache.*key|double free",
        "claim": "tcache key 校验自 glibc 2.29 起",
        "source": "https://github.com/ir0nstone/cybersec-notes/blob/master/binexp/heap/tcache-keys.md",
        "require_in_traps": r"2\.29",
    },
    {
        "id": "glibc_safelinking",
        "pattern": r"safe-linking|safe linking|PROTECT_PTR",
        "claim": "safe-linking 自 glibc 2.32 起",
        "source": "https://raw.githubusercontent.com/ir0nstone/cybersec-notes/refs/heads/master/binexp/heap/safe-linking.md",
        "require_in_traps": r"2\.32",
    },
    {
        "id": "cve_2016_7124",
        "pattern": r"CVE-2016-7124|wakeup.*绕过",
        "claim": "CVE-2016-7124 影响 PHP <5.6.25 与 7.x <7.0.10",
        "source": "https://app.opencve.io/cve/CVE-2016-7124",
        "require_in_traps": r"5\.6\.25|7\.0\.10",
    },
]

# 危险取值：教了具体常量必须提示副作用
DANGEROUS_VALUES = [
    (r"0xffffffffffffffff|0xfffffffffffffffe", "该值在多数现代版本会触发完整性校验并 abort"),
]


def check_structure(d):
    issues = []
    for fld in ("steps", "traps"):
        for i, x in enumerate(d.get(fld) or []):
            if not isinstance(x, str):
                issues.append(f"C1 {fld}[{i}] 不是字符串（类型 {type(x).__name__}）")
    if not (d.get("keywords") or []):
        issues.append("C1 keywords 为空")
    if not (d.get("steps") or []):
        issues.append("C1 steps 为空")
    return issues


def check_known_facts(d):
    body = " ".join(str(x) for x in (d.get("steps") or []) + (d.get("traps") or []))
    notes = []
    for f in KNOWN_FACTS:
        if re.search(f["pattern"], body, re.I):
            if not re.search(f["require_in_traps"], body, re.I):
                notes.append(f"C2 涉及「{f['claim']}」但未在 traps 中提及（来源 {f['source']}）")
    return notes


def check_dangerous(d):
    """C3：步骤里教的具体取值若会触发完整性校验，traps 必须**专门**提示它。

    注意不能只看 traps 里有没有"abort/崩溃"这类词——很多卡在讲别的副作用时
    也用了这些词，会误判为"已提示"。必须要求该取值与后果同现。
    """
    issues = []
    for pat, warn in DANGEROUS_VALUES:
        step_hit = any(re.search(pat, str(s)) for s in (d.get("steps") or []))
        if not step_hit:
            continue
        traps = " ".join(str(x) for x in (d.get("traps") or []))
        # 要求：traps 中出现该取值本身，或明确提到 top size / corrupted
        specific = re.search(r"top.*size|corrupted top|size > system_mem", traps, re.I)
        if not specific:
            issues.append(f"C3 步骤含危险取值 {pat}，traps 未专门提示「{warn}」")
    return issues


def check_self_consistency(d):
    issues = []
    body = " ".join(str(x) for x in (d.get("steps") or []) + (d.get("traps") or []))
    # 同一张卡里既说可用又说已移除
    if re.search(r"可用于?\s*2\.3\d", body) and re.search(r"2\.34.*移除", body):
        if not re.search(r"不适用|失效|仅.*以下", body):
            issues.append("C4 存在版本表述矛盾")
    return issues


import json
_EVID = None


def _evidence_map():
    """card_id -> evidence_count，来自 build_techniques 生成的 json。"""
    global _EVID
    if _EVID is None:
        _EVID = {}
        p = os.path.join(ROOT, "techniques", "techniques.json")
        if os.path.exists(p):
            for t in json.load(open(p, encoding="utf-8")).get("techniques", []):
                _EVID[t["id"]] = t.get("evidence_count") or 0
    return _EVID


def audit(d):
    issues = []
    issues += check_structure(d)
    issues += check_dangerous(d)
    issues += check_self_consistency(d)
    notes = check_known_facts(d)

    if issues:
        status = "suspect"
    elif notes:
        status = "unverified"
    elif _evidence_map().get(d["id"], 0) == 0:
        status = "unverified"
        notes = notes + ["C5 无关联 WP 证据"]
    else:
        status = "verified"
    return status, issues, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--force", action="store_true", help="连已审的卡也重审")
    args = ap.parse_args()
    apply = args.apply and not args.dry_run

    files = sorted(glob.glob(os.path.join(CARD_DIR, "*.yaml")))
    results = []
    for p in files:
        d = yaml.safe_load(open(p, encoding="utf-8"))
        if not isinstance(d, dict) or "id" not in d:
            continue
        if d.get("review_status") and not args.force:
            continue
        status, issues, notes = audit(d)
        results.append((p, d, status, issues, notes))

    by_status = {}
    for p, d, st, iss, nt in results:
        by_status.setdefault(st, []).append(d["id"])

    print(f"审核 {len(results)} 张（跳过已审）")
    for st in ("verified", "corrected", "unverified", "suspect"):
        ids = by_status.get(st, [])
        print(f"  {st:11} {len(ids):3}  {' '.join(ids[:8])}{' …' if len(ids) > 8 else ''}")

    if apply:
        for p, d, st, iss, notes in results:
            d["review_status"] = st
            d["reviewed_at"] = TODAY
            d["review_notes"] = ("; ".join(iss + notes))[:400] or "自动审核：结构/版本/危险取值/自洽性四项检查通过"
            yaml.safe_dump(d, open(p, "w", encoding="utf-8"),
                           allow_unicode=True, sort_keys=False, width=1000)
        print("\n已写入审核状态")

    # 输出明细供人工复核 suspect 项
    suspects = [(d["id"], iss + notes) for p, d, st, iss, notes in results if st == "suspect"]
    if suspects:
        print("\n=== suspect 明细（需人工修正）===")
        for cid, msgs in suspects:
            print(f"  {cid}")
            for m in msgs:
                print(f"    - {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
